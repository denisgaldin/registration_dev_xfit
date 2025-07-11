pipeline {
    agent any

    environment {
        BASE_URL = 'https://dev-mobile.xfit.ru'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your/repo.git', branch: 'main'  // Укажи свой репо
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/ --junitxml=report.xml -v'
            }
            post {
                always {
                    junit 'report.xml'
                    archiveArtifacts artifacts: 'report.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo '✅ Тесты успешно прошли!'
        }
        failure {
            echo '❌ Тесты упали!'
        }
        always {
            echo 'Пайплайн завершён.'
        }
    }
}
