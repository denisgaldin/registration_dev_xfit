pipeline {
    agent any

    environment {
        BASE_URL = 'https://dev-mobile.xfit.ru'  // URL твоего API
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your/repo.git', branch: 'main'  // замени на свой репозиторий
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
                    junit 'report.xml'  // публикация отчётов JUnit
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
