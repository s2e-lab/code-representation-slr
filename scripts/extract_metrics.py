import sqlite3
import pandas as pd

conn = sqlite3.connect('../analyses/db_survey_representations.sqlite3')

cursor = conn.cursor()

def get_evaluation_metrics(user_id):
    query = """
    SELECT 
        m.name AS metric_name, 
        er.value
    FROM 
        survey_representations_evaluationresult er
    JOIN 
        survey_representations_metric m ON er.metric_id = m.id
    JOIN 
        survey_representations_analysis a ON er.analysis_id = a.id
    WHERE 
        a.user_id = ? AND m.name IN ('Precision', 'Recall', 'F1 score');
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


# Function to get representation and task for user ID #10
def get_representation_and_task(user_id):
    query = """
    SELECT 
        r.name AS representation, 
        t.name AS task
    FROM 
        survey_representations_analysis a
    JOIN 
        survey_representations_representation r ON r.id IN (SELECT representation_id FROM survey_representations_analysis_representations WHERE analysis_id = a.id)
    JOIN 
        survey_representations_cybersecuritytask t ON t.id IN (SELECT cybersecuritytask_id FROM survey_representations_analysis_tasks WHERE analysis_id = a.id)
    WHERE 
        a.user_id = ?;
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

# Function to get aggregated metrics by representation per task for user ID #10
def get_aggregated_metrics(user_id):
    query = """
    SELECT 
    r.name AS representation,
    t.name AS task,
    AVG(CASE WHEN m.name = 'Precision' THEN er.value END) AS avg_precision,
    AVG(CASE WHEN m.name = 'Recall' THEN er.value END) AS avg_recall,
    AVG(CASE WHEN m.name = 'F1 score' THEN er.value END) AS avg_f1,
    COUNT(CASE WHEN m.name = 'Precision' THEN er.value END) AS count_precision,
    COUNT(CASE WHEN m.name = 'Recall' THEN er.value END) AS count_recall,
    COUNT(CASE WHEN m.name = 'F1 score' THEN er.value END) AS count_f1
FROM 
    survey_representations_analysis a
JOIN 
    survey_representations_representation r ON r.id IN (SELECT representation_id FROM survey_representations_analysis_representations WHERE analysis_id = a.id)
JOIN 
    survey_representations_cybersecuritytask t ON t.id IN (SELECT cybersecuritytask_id FROM survey_representations_analysis_tasks WHERE analysis_id = a.id)
JOIN 
    survey_representations_evaluationresult er ON er.analysis_id IN (SELECT id FROM survey_representations_analysis WHERE paper_id = a.paper_id)
JOIN 
    survey_representations_metric m ON er.metric_id = m.id
WHERE 
    a.user_id = 10  -- For representations and tasks
    AND er.analysis_id IN (SELECT id FROM survey_representations_analysis WHERE user_id = 5)  -- For metrics from user ID 5
GROUP BY 
    r.name, t.name;

    """
    cursor.execute(query)
    return cursor.fetchall()

beatrice = 5
slr_merger = 10

evaluation_metrics = get_evaluation_metrics(beatrice)
representation_and_task = get_representation_and_task(slr_merger)
aggregated_metrics = get_aggregated_metrics(slr_merger)


# Print results
print("Evaluation Metrics for User ID #5:")
for metric in evaluation_metrics:
    print(f"{metric[0]}: {metric[1]}")

print("\nRepresentation and Task for User ID #10:")
for representation, task in representation_and_task:
    print(f"Representation: {representation}, Task: {task}")

print("\nAggregated Metrics for User ID #10:")
for row in aggregated_metrics:
    print(f"Representation: {row[0]}, Task: {row[1]}, "
          f"Avg Precision: {row[2]}, Avg Recall: {row[3]}, Avg F1: {row[4]}")

columns = ['Representation', 'Task', 'Avg Precision', 'Avg Recall', 'Avg F1', 'Count Precision', 'Count Recall', 'Count F1']

# Create a DataFrame from the results
df = pd.DataFrame(aggregated_metrics, columns=columns)

# Export the DataFrame to a CSV file
df.to_csv('aggregated_metrics_with_counts.csv', index=False)

print("Results exported to aggregated_metrics.csv")

# close the connection
conn.close()