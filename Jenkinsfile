pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        VENV_DIR = 'venv'
        HEADLESS = 'true'
        BROWSER = 'chrome'
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

        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python --version
                    pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Executing pytest test suite in headless mode...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p reports screenshots
                    pytest tests/ \
                        --headless \
                        --browser=${BROWSER} \
                        --html=reports/report.html \
                        --self-contained-html \
                        -v
                '''
            }
        }

        stage('Generate HTML Report') {
            steps {
                echo 'Verifying HTML report was generated...'
                sh '''
                    if [ ! -f reports/report.html ]; then
                        echo "ERROR: HTML report not found at reports/report.html"
                        exit 1
                    fi
                    echo "HTML report generated successfully."
                    ls -la reports/
                '''
            }
        }
    }

    post {
        always {
            echo 'Archiving test artifacts...'
            archiveArtifacts artifacts: 'reports/**/*.html', allowEmptyArchive: false
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully. All tests passed.'
        }
        failure {
            echo 'Pipeline failed. Review archived reports and screenshots.'
        }
    }
}
