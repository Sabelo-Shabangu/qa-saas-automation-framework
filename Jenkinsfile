pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        HEADLESS = 'true'
        BASE_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
        TEST_USERNAME = 'Admin'
        TEST_PASSWORD = 'admin123'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                bat """
                    python -m venv %VENV_DIR%

                    call %VENV_DIR%\\Scripts\\activate

                    python --version
                    pip install --upgrade pip
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'

                bat """
                    call %VENV_DIR%\\Scripts\\activate

                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Selenium PyTest suite...'

                bat """
                    call %VENV_DIR%\\Scripts\\activate

                    if not exist reports mkdir reports
                    if not exist screenshots mkdir screenshots

                    pytest tests ^
                    --html=reports/report.html ^
                    --self-contained-html ^
                    -v
                """
            }
        }
    }

    post {

        always {

            echo 'Publishing reports and archiving artifacts...'

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'QA Automation Report'
            ])

            archiveArtifacts artifacts: 'reports/*.html, screenshots/*.png',
                             allowEmptyArchive: true
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Review console logs and screenshots.'
        }
    }
}