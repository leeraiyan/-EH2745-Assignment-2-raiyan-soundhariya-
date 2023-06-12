from application import app
from flask import render_template, url_for, redirect,flash, get_flashed_messages
from application.form import UserDataForm
from application.models import IncomeExpenses
from application import db
from application.DataGenerator import *
from application.Agent_KMeans import *
from application.GraphPlotter import *
from application.Agent_KNN import *
import csv
import json
import os
import pandas as pd
import numpy as np


caseInteger = {
    'normal_operation': 1,
    'high_load': 2,
    'low_load': 3,
    'disconnect_generator_3_high': 4,
    'disconnect_generator_3_low': 5,
    'disconnect_line_bus_5_6_high': 6,
    'disconnect_line_bus_5_6_low': 7

}


@app.route('/loading')
def loading_screen():
    return render_template('loading.html')

@app.route('/', methods = ["POST", "GET"])
def index():
    form = UserDataForm()
    if form.validate_on_submit():
        #delete all entries in the database
        db.session.query(IncomeExpenses).delete()

        #delete all existing data as well
        directory_path = './data'  # Replace with the path to the directory you want to delete
        try:
            # Delete the directory
            os.rmdir(directory_path)
            
        except OSError as e:
            print( f'Error deleting directory: {str(e)}' ) 

        # Prepare new data using data generator
        # Data generator writes output data into xlsx files
        datagenerator = DataGenerator()
        datagenerator.source_network()
        combined_df = pd.DataFrame(columns=['vm1','vm2','vm3','vm4','vm5','vm6','vm7','vm8','vm9',
               'degree1','degree2','degree3','degree4','degree5','degree6','degree7','degree8','degree9'])
        labels = []


        # Read all generated data from xlsx files
        # Store them into database
        for case in form.example.data:
            datagenerator.simulate(case,70)
            
            df_mag = pd.read_excel(f'./data/{case}/res_bus/vm_pu.xlsx')
            df_mag = df_mag.drop(columns=['Unnamed: 0'])
            new_column_names = ['vm1', 'vm2', 'vm3', 'vm4', 'vm5', 'vm6', 'vm7', 'vm8', 'vm9']
            df_mag.rename(columns=dict(zip(df_mag.columns[0:9], new_column_names)), inplace=True)

            df_deg = pd.read_excel(f'./data/{case}/res_bus/va_degree.xlsx')
            df_deg = df_deg.drop(columns=['Unnamed: 0'])
            new_column_names = {0: 'degree1', 1: 'degree2', 2: 'degree3', 3: 'degree4', 4: 'degree5', 5: 'degree6', 6: 'degree7', 7: 'degree8', 8: 'degree9'}
            df_deg.rename(columns=new_column_names, inplace=True)
            concatenated_df = pd.concat([df_mag, df_deg], axis=1)
            
            for index, row in concatenated_df.iterrows():
                counter = 0
                voltage_mag = ""
                voltage_ang = ""
                for column_name, cell_value in row.items():
                    counter += 1
                    if counter < 10:
                        voltage_mag += str(cell_value) + ", "
                    else:
                        voltage_ang += str(cell_value) + ", "
                entry = IncomeExpenses(type=voltage_mag, category=voltage_ang, amount=caseInteger[case])
                labels.append(caseInteger[case])
                db.session.add(entry)
            
            concatenated_df.reset_index(drop=True, inplace=True)
            combined_df = pd.concat([combined_df, concatenated_df], ignore_index=True)
        db.session.commit()



        # Execute the query to fetch data from the database
        # Store all information into csv file for agents to use
        query = db.session.query(IncomeExpenses).all()
        csv_file_path = 'check.csv'
        # Open the CSV file in write mode
        with open(csv_file_path, 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)
            for row in query:
                vm = row.type.split(",")

                va = row.category.split(",")
                writer.writerow([vm[0],vm[1],vm[2],vm[3],vm[4],vm[5],vm[6],vm[7],vm[8],
                                  va[0],va[1],va[2],va[3],va[4],va[5],va[6],va[7],va[8],
                                  row.amount])


        # Instantiate agent for KMeans clustering
        # Run algorithm
        agentkmeans = AgentKMeans()
        k, J_r, means_r, final_cluster = agentkmeans.kmeans_clustering(combined_df)

        # Instantiate agent for KNN classifier
        # Run algorithm
        agentknn = AgentKNN()
        agentknn.KNN()

        # Plot results in matplotlib
        plotter = GraphPlotter()
        plotter.plot(combined_df, final_cluster) 
        
        flash(f"Success! Generated data for {len(form.example.data)} cases, 70 datapoints each", 'success')
        return redirect(url_for('add_expense'))
    return render_template('index.html', title="Input Data", form=form)


@app.route('/data')
def add_expense():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('data.html', entries = entries)
    


@app.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("add_expense"))


@app.route('/dashboard')
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expense:
        income_expense.append(total_amount)

    over_time_expenditure = []
    dates_label = []
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)

    return render_template('dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label)
                        )