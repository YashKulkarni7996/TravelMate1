pipeline {
    agent any

    environment {
        APP_NAME = 'student-info-app'
        PYTHON = 'python' // Use 'python3' if that's your command
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Cloning repository...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up virtual environment...'
                bat """
                ${env.PYTHON} -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        // stage('Run Tests') {
        //     steps {
        //         echo '🧪 Running tests (if any)...'
        //         bat """
        //         call venv\\Scripts\\activate
        //         pytest tests || echo No tests found.
        //         """
        //     }
        // }

        stage('Deploy Locally') {
            steps {
                echo '🚀 Launching Streamlit app locally...'
                bat """
                call venv\\Scripts\\activate
                start /B streamlit run app.py --server.port=8501
                """
            }
        }
    }

    post {
        success {
            echo '✅ Deployment completed successfully! Visit http://localhost:8501'
        }
        failure {
            echo '❌ Deployment failed. Check logs for details.'
        }
    }
}
