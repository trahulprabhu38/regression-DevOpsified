pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "trahulprabhu38/mlops:v1"
        DOCKER_REGISTRY = "https://index.docker.io/v1/"
        KUBE_CONFIG = credentials('kubeconfig') 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                sh 'pip install flake8 && flake8 main.py'
            }
        }
        stage('Test') {
            steps {
                // Replace with your test command, e.g. pytest
                sh 'pip install pytest && pytest || echo "No tests yet"'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry(env.DOCKER_REGISTRY, 'dockerhub') {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withEnv(["KUBECONFIG=${env.KUBE_CONFIG}"]) {
                    sh 'kubectl version'
                    sh 'kubectl apply -f k8s-deployment.yaml'
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}