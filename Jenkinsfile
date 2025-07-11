pipeline {
    agent any

    environment {
        BASE_URL = 'https://dev-mobile.xfit.ru'  //
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your/repo.git', branch: 'main'  // замени на свой
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'  // для отображения результатов тестов в Jenkins
                }
            }
        }
    }
}
