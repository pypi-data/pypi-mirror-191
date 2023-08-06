import requests
import json

class Url:
    def __init__(self, url) -> None:
        self.__url = url

    def __str__(self):
        return self.__url

    def _repr_html_(self):
        """HTML link to this URL."""
        return f'<a href="{self.__url}">{self.__url}</a>'

class ArmillaClient:
    def __init__(self, username, password, env="PRODUCTION"):
        self.base_url, self.url = self._get_url_from_env(env)
        self.username = username
        self.password = password
        self.auth_token = self._get_auth_token(username, password)

    def _get_headers(self):
        return {
            "Authorization": self.auth_token
        }

    def _get_url_from_env(self, env):
        if env == "PRODUCTION":
            return ("https://app.hosted.armilla.ai/", "https://app.hosted.armilla.ai/backend/")
        elif env == "STAGING":
            return ("https://app.staging.armilla.ai/", "https://app.staging.armilla.ai/backend/")
        elif env == "DEMO":
            return ("https://app.demo.armilla.ai/", "https://app.demo.armilla.ai/backend/")
        elif env == "LOCAL":
            return ("http://127.0.0.1:3000/", "http://127.0.0.1:8000/")
        else:
            raise Exception("Not a valid env: (PRODUCTION, STAGING, DEMO, LOCAL")

    def run(self, run_name, model_id, test_plan_id, project_id):
        """
            Trigger an analysis run from a project's test plan + model

                Parameters:
                    run_name: name of test run shown on project
                    model_id: id of model in project
                    test_plan_id: id of project test plan to run
                    project_id: project id
                Returns:
                    response: model object from response
        """
        request_url = self.url + "api/testPlanRuns/"
        headers = self._get_headers()
        request_body = {
            "modelDefinitionId": model_id,
            "name": run_name,
            "project": project_id,
            "testPlanId": test_plan_id
        }
        response = requests.post(request_url, data=request_body, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to trigger run")
        else:
            return_response = response.json()
            return self._build_test_run_url(project_id, return_response["id"])
    
    def upload_model(
        self,
        model_name,
        model_path,
        runner_type,
        project_id,
        model_source_type="FILE_SYSTEM",
        tokenizer_path=None,
        tokenizer_source="FILE_SYSTEM",
        tokenizer_type=None,
        description=""
    ):
        """
            upload a model from local file path to a project

                Parameters:
                    model_name: name of model shown on project
                    model_path: local file path of the model file
                    runner_type: type of model runner
                    project_id: project id
                    model_source_type: source type of the model, defaults to FILE_SYSTEM (local uploaded), also supported "REMOTE"
                    tokenizer_path: (optional) provide if the model definition requires tokenizer
                    tokenizer_source: provide to set tokenizer source, defaults to FILE_SYSTEM (local uploaded), also supported "REMOTE"
                    tokenizer_type: (optional) provide if tokenizer uploaded, supported "Dict" or "Keras"
                Returns:
                    response: model object from response
        """
        request_url = self.url + "api/modelDefinitions/"
        response = None
        headers = self._get_headers()
        if model_source_type == "REMOTE":
            request_body = {
                "modelName": model_name,
                "description": description,
                "runnerType": runner_type,
                "project": project_id,
                "modelLocationType": model_source_type,
                "filepath": model_path
            }
            if tokenizer_path:
                request_body["tokenizer_path"] = tokenizer_path
                request_body["tokenizer_location_type"] = tokenizer_source
                request_body["tokenizer_type"] = ""
            response = requests.post(request_url, data=request_body, headers=headers)

        elif model_source_type == "FILE_SYSTEM":
            request_body = {
                "modelName": model_name,
                "description": description,
                "runnerType": runner_type,
                "project": project_id,
                "modelLocationType": model_source_type
            }
            model_file = open(model_path, 'rb')
            file_body = {
                "file": model_file,
            }

            tokenizer_file = None
            if tokenizer_path:
                tokenizer_file = open(tokenizer_path, 'rb')
                request_body["tokenizer_path"] = tokenizer_path
                request_body["tokenizer_location_type"] = tokenizer_source
                request_body["tokenizer_type"] = tokenizer_type
                file_body["tokenizer_file"] = tokenizer_file
            
            response = requests.post(request_url, files=file_body, data=request_body, headers=headers)

            model_file.close()
            if tokenizer_file:
                tokenizer_file.close()
        else:
            raise Exception("source type not supported")

        return response.json()

    def upload_data_set(self, dataset_name, dataset_path, project_id, description="", source_type="E", window_size=None, expected_labels_path=None):
        """
            upload a dataset from local file path to a project

                Parameters:
                    dataset_name: name of dataset shown on project
                    dataset_path: local file path of the dataset file
                    project_id: project id
                Returns:
                    response: dataset object from response
        """
        request_url = self.url + "api/datasets/"
        headers = self._get_headers()
        dataset_file = open(dataset_path, 'rb')
        file_body = {
            "file": dataset_file
        }
        expected_label_file=None
        if expected_labels_path:
            expected_label_file = open(expected_labels_path, 'rb')
            file_body["expected_labels_file"] = expected_label_file

        request_body = {
            "sourceType": source_type,
            "datasetName": dataset_name,
            "datasetLocationType": "FILE_SYSTEM",
            "description": description,
            "project": project_id,
            "window_size": window_size
        }
        response = requests.post(request_url, files=file_body, data=request_body, headers=headers)

        dataset_file.close()
        if expected_label_file:
            expected_label_file.close()

        return response.json()
    
    def create_project(self, project_name, model_type, description=""):
        """
            create a new project

                Parameters:
                    project_name: name of the new project
                    model_type: model type of the project
                    description: optionally provide description
        """
        request_url = self.url + "api/projects/"
        headers = self._get_headers()
        request_body = {
            "name": project_name,
            "model_type": model_type,
            "description": description
        }
        response = requests.post(request_url, data=request_body, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to create a project")

        return response.json()

    def create_data_dictionary(self, dataset_path, project_id):
        """
            generate the data dictionary, using this will replace existing features

                Parameters:
                    dataset_path: local path of dataset used to infer data dictionary
                    project_id: project id
        """
        request_url = self.url + "api/features/"
        headers = self._get_headers()

        with open(dataset_path, 'rb') as f:
            file_body = {
                "file": f
            }
            request_body = {
                "project_id": project_id,
                "file_type": "csv"
            }
            response = requests.post(request_url, files=file_body, data=request_body, headers=headers)
            return response.json()

    def update_data_dictionary(
        self,
        project_id,
        expected_outcome=None,
        favorable_outcome=None,
        unfavorable_outcome=None,
        privileged_attributes=None,
        unprivileged_attributes=None,
        privileged_buckets=None,
        unprivileged_buckets=None,
        excluded_features=None,
        feature_type=None,
        fairness_type=None,
    ):
        """
            updates data dictionary by providing necessary feature information

                Parameters:
                    project_id: project_id
                    expected_outcome: str, feature name of expected outcome
                    favorable_outcome: list[str], list of favorable outcome classes - must provide expected_outcome
                    unfavorable_outcome: list[str], list of unfavorable outcome classes - must provide expected_outcome
                    privileged_attributes: dictionary, key - feature name, value - list of values considered priviledged
                    unprivileged_attributes: dictionary, key - feature name, value - list of values considered unprivileged
                    priviledged_buckets: dictionary, range of continuous values considered priviledged
                    unpriviledged_buckets: dictionary, range of continuous values considered priviledged
                    excluded_features: list[str], list of features considered excluded
        """
        request_url = self.url + "api/features/"
        headers = self._get_headers()

        data_dictionary = self.get_data_dictionary(project_id=project_id)

        if (favorable_outcome or unfavorable_outcome) and not expected_outcome:
            raise Exception("setting favorable_outcome and unfavorable outcome requires providing expected_outcome")

        features_to_update = {}
        if expected_outcome:
            features_to_update[expected_outcome] = {
                "outcome": True
            }

            if favorable_outcome:
                features_to_update[expected_outcome]["priviledged_predictions"] = favorable_outcome
            
            if unfavorable_outcome:
                features_to_update[expected_outcome]["unpriviledged_predictions"] = unfavorable_outcome
        
        if privileged_attributes:
            for feature_name, privileged_vals in privileged_attributes.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["priviledged_groups"] = privileged_vals
                
        if unprivileged_attributes:
            for feature_name, unprivileged_vals in unprivileged_attributes.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["unpriviledged_groups"] = unprivileged_vals
        
        if excluded_features:
            for feature_name in excluded_features:
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["excluded"] = True
        
        if feature_type:
            for feature_name, f_type in feature_type.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["feature_type"] = f_type
        
        if fairness_type:
            for feature_name, fair_type in fairness_type.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["fairness_type"] = fair_type
        
        if privileged_buckets:
            for feature_name, bucket in privileged_buckets.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["privileged_buckets"] = bucket
        
        if unprivileged_buckets:
            for feature_name, bucket in unprivileged_buckets.items():
                features_to_update.setdefault(feature_name, {})
                features_to_update[feature_name]["unprivileged_buckets"] = bucket

        for feature in data_dictionary:
            if feature["name"] in features_to_update:
                features_to_update[feature["name"]]["id"] = feature["id"]
        
        for feature_name, feature_info in features_to_update.items():
            id = feature_info.pop("id", None)
            if not id:
                raise Exception("The feature that's needs to be updated does not exist in data dictionary: " + feature_name)
            
            feature_url = request_url + str(id) + "/"
            response = requests.put(feature_url, json=feature_info, headers=headers)
            if response.status_code != 200:
                raise Exception("Error updating feature: " + feature_name)
        
        return self.get_data_dictionary(project_id=project_id)
    
    def create_new_test_plan(self, test_plan_name, project_id):
        """
            create a new blank test plan inside a project

                Parameters:
                    test_plan_name: name of the test plan
                    project_id: project id
        """
        request_url = self.url + "api/testPlans/"
        headers = self._get_headers()

        request_body = {
            "name": test_plan_name,
            "projectId": project_id,
        }
        response = requests.post(request_url, data=request_body, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to create a test plan")
        return response.json()

    def update_test_plan_scenarios(self, test_plan_id, dataset_ids, pipeline_config):
        """
            Update the configuration of dataset_ids in test plan

                Parameters:
                    test_plan_id: id of the test plan to update
                    dataset_ids: list of ids to attach pipeline config to
                    pipeline_config: a dictionary of pipeline configuration
        """

        request_url = self.url + "api/testPlans/" + str(test_plan_id) + "/"
        headers = self._get_headers()

        if (type(pipeline_config) is not dict):
            raise Exception("pipeline config must be a python dictionary")

        test_plan = self.get_test_plan(test_plan_id)
        dataset_ids = set(dataset_ids)

        updated_scenarios = []

        for scenario in test_plan["scenarios"]:
            if scenario["data_source"] in dataset_ids:
                scenario_content = scenario
                scenario_content["test_pipelines"] = pipeline_config
                updated_scenarios.append(scenario_content)
                dataset_ids.remove(scenario["data_source"])
        
        for new_data_source in dataset_ids:
            scenario_content = {
                "data_source": new_data_source,
                "enabled": True,
                "test_pipelines": pipeline_config
            }
            updated_scenarios.append(scenario_content)
        
        request_body = {
            "scenarios": json.dumps(updated_scenarios)
        }

        response = requests.put(request_url, json=request_body, headers=headers)

        if response.status_code != 200:
            raise Exception("failed to update test plan")

        return response.json()

    def get_projects(self):
        request_url = self.url + "api/projects/"
        headers = self._get_headers()
        response = requests.get(request_url, headers=headers).json()

        projects = []
        for result in response["results"]:
            projects.append({
                "id": result["id"],
                "name": result["name"],
                "description": result["description"],
                "model_type": result["model_type"]
            })

        return projects
    
    def get_project_summary(self, project_id):
        request_url = self.url + "api/projects/" + str(project_id) + "/"
        headers = self._get_headers()
        response = requests.get(request_url, headers=headers)

        if response.status_code != 200:
            return Exception("Failed to fetch project")
        
        project_response = response.json()
        project_summary = {
            "id": project_response["id"],
            "name": project_response["name"],
            "description": project_response["description"],
            "model_type": project_response["model_type"]
        }

        request_url = self.url + "api/modelDefinitions/"
        params = {
            "project": project_id
        }

        response = requests.get(request_url, headers=headers, params=params).json()

        model_definitions = []
        for result in response["results"]:
            model_definitions.append({
                "id": result["id"],
                "name": result["name"],
                "description": result["description"],
                "runner_type": result["runner_type"],
                "prediction_type": result["prediction_type"]
            })
        
        project_summary["model_definitions"] = model_definitions

        request_url = self.url + "api/datasets/"
        params = {
            "project": project_id
        }
        response = requests.get(request_url, headers=headers, params=params).json()

        datasets = []
        for result in response["results"]:
            datasets.append({
                "id": result["id"],
                "name": result["name"]
            })
        project_summary["datasets"] = datasets

        return project_summary
    
    def get_data_dictionary(self, project_id):
        request_url = self.url + "api/features/"
        headers = self._get_headers()
        params = {
            "project": project_id
        }

        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch data dictionary")
        
        feature_count = response.json()["count"]
        PAGE_SIZE = 10
        page_count = int(feature_count / PAGE_SIZE) + (feature_count % PAGE_SIZE > 0)
        result = []

        for page_num in range(0, page_count):
            params["page"] = page_num + 1
            response = requests.get(request_url, headers=headers, params=params)
            if response.status_code != 200:
                Exception("Failed to fetch data dictionary")
            result.extend(response.json()["results"])
        
        return result

    def get_runs_for_project(self, project_id):
        request_url = self.url + "api/testPlanRuns/"
        headers = self._get_headers()
        params = {
            "project": project_id
        }

        response = requests.get(request_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch runs")
        else:
            return_response = []
            for run in response.json()["results"]:
                run["run_url"] = str(self._build_test_run_url(run["project"], run["id"]))
                return_response.append(run)

        return return_response

    def get_test_plans_for_project(self, project_id):
        request_url = self.url + "api/testPlans/"
        headers = self._get_headers()
        params = {
            "project": project_id
        }

        response = requests.get(request_url, headers=headers, params=params)
        return response.json()["results"]
    
    def get_test_plan(self, test_plan_id):
        request_url = self.url + "api/testPlans/" + str(test_plan_id) + "/"
        headers = self._get_headers()

        response = requests.get(request_url, headers=headers)
        return response.json()
    
    def _get_auth_token(self, username, password):
        '''
        Authenticates user request and returns auth token if successful

            Parameters:
                username: user login
                password: user password
            Returns:
                token: bearer token for client requests
        '''
        request_url = self.url + "api/request_token/"
        params = {
            "username": username,
            "password": password
        }
        if username is None:
            raise Exception("username required")
        if password is None:
            raise Exception("password required")

        response = requests.post(request_url, data=params)
        if response.status_code == 403:
            raise Exception(response.json())
        if response.status_code != 200:
            raise Exception("error requesting token")

        token = response.json()["token_type"] + " " + response.json()["access_token"]
        return token
    
    def _build_test_run_url(self, project_id, run_id):
        url = "{base_url}{project_id}/runs/{run_id}?selectedBucket=Fingerprint&selectedPipeline=TEST_ANALYSIS_SUMMARY".format(
            base_url=self.base_url,
            project_id=str(project_id),
            run_id=str(run_id)
        )
        return Url(
            url=url
        )
