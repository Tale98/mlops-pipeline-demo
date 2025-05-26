import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle
import shutil
script_path = os.path.dirname(os.path.abspath(__file__))
# ENV config 
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
exp_name = "iris-demo"

# Ensure the experiment exists (create if not)
try:
    mlflow.create_experiment(
        name=exp_name,
        artifact_location=os.environ.get("MLFLOW_ARTIFACT_ROOT", "s3://mlflow")
    )
except Exception:
    pass
## create temporary directory for artifacts
os.makedirs(os.path.join(script_path, 'temp'), exist_ok=True)
os.chdir(os.path.join(script_path, 'temp'))
# try:
mlflow.set_experiment(exp_name)
with mlflow.start_run(run_name="sklearn-demo"):
    # 1. Load Data
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # 2. Train Model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # 3. Predict & Metrics
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc)
    # Log classification report as artifact
    report = classification_report(y_test, y_pred, output_dict=True)
    with open("clf_report.txt", "w") as f:
        f.write(classification_report(y_test, y_pred))
    mlflow.log_artifact("clf_report.txt")

    # Log simple plot as artifact
    plt.figure()
    plt.bar(data.target_names, [sum(y_test==i) for i in range(3)])
    plt.title("Test set class distribution")
    plt.savefig("class_dist.png")
    mlflow.log_artifact("class_dist.png")

    # Log trained model as artifact (pickle)
    with open("rf_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    mlflow.log_artifact("rf_model.pkl")

    # Optionally, log model via mlflow API (for later serving)
    mlflow.sklearn.log_model(clf, "sklearn-model")
# except:
#     print("An error occurred during the MLflow run.")
## remove temporary directory
shutil.rmtree(os.path.join(script_path, 'temp'))