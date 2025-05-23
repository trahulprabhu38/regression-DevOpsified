pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        TF_DIR = 'terraform'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Terraform Format & Lint') {
            steps {
                dir("${env.TF_DIR}") {
                    sh "terraform fmt -check -recursive"
                }
            }
        }
        stage('Terraform Init') {
            steps {
                dir("${env.TF_DIR}") {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins-creds']]) {
                        sh '''
                            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                            terraform init -input=false
                        '''
                    }
                }
            }
        }
        stage('Terraform Validate') {
            steps {
                dir("${env.TF_DIR}") {
                    sh "terraform validate"
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                dir("${env.TF_DIR}") {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins-creds']]) {
                        sh '''
                            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                            terraform plan -out=tfplan
                        '''
                    }
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                input "Approve to apply Terraform changes?"
                dir("${env.TF_DIR}") {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins-creds']]) {
                        sh '''
                            export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                            export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                            terraform apply -auto-approve tfplan
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Terraform pipeline completed successfully!'
        }
        failure {
            echo 'Terraform pipeline failed.'
        }
    }
}