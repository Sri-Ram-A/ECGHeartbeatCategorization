
def get_next_run_number(experiment_name, tracking_uri):
    """Get next run number for the experiment"""
    try:
        from mlflow.tracking import MlflowClient
        client = MlflowClient(tracking_uri)
        experiment = client.get_experiment_by_name(experiment_name)
        
        if experiment:
            runs = client.search_runs(experiment_ids=[experiment.experiment_id])
            return len(runs)+1
    except:
        pass
    return 1