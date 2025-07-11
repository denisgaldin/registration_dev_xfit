pipeline {
    agent any

    environment {
        DOTENV_PATH = '.env'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv $PYTHON_ENV
                source $PYTHON_ENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source $PYTHON_ENV/bin/activate
                # Загружаем переменные из .env в окружение
                export $(grep -v '^#' $DOTENV_PATH | xargs)
                pytest tests/ --tb=short -v --junitxml=reports/results.xml
                '''
            }
            post {
                always {
                    junit 'reports/results.xml'
                    archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        success {
            echo 'Тесты прошли успешно!'
        }
        failure {
            echo 'Тесты упали!'
        }
    }
}
