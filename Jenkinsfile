pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        DOCKER_IMAGE = 'trahulprabhu38/mlops:v1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup SSH Keys') {
            steps {
                sh 'mkdir -p terraform/infrastructure/keys'
                withCredentials([sshUserPrivateKey(credentialsId: 'aws-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh 'cp $SSH_KEY terraform/infrastructure/keys/aws-key'
                    sh 'chmod 600 terraform/infrastructure/keys/aws-key'
                }
                withCredentials([file(credentialsId: 'aws-ssh-key-pub', variable: 'SSH_PUB_KEY')]) {
                    sh 'cp $SSH_PUB_KEY terraform/infrastructure/keys/aws-key.pub'
                }
            }
        }

        stage('Bootstrap Terraform') {
            steps {
                dir('terraform/bootstrap') {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-key'
                    ]]) {
                        sh 'terraform init -input=false'
                        sh 'terraform validate'
                        sh 'terraform plan -out=tfplan'
                        sh 'terraform apply -auto-approve tfplan'
                    }
                }
            }
        }

        stage('Infrastructure Terraform Init') {
            steps {
                dir('terraform/infrastructure') {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-key'
                    ]]) {
                        sh 'terraform init -input=false'
                    }
                }
            }
        }

        stage('Infrastructure Terraform Validate') {
            steps {
                dir('terraform/infrastructure') {
                    sh 'terraform validate'
                }
            }
        }

        stage('Infrastructure Terraform Plan') {
            steps {
                dir('terraform/infrastructure') {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-key'
                    ]]) {
                        sh 'terraform plan -var="docker_image=${DOCKER_IMAGE}" -out=tfplan'
                    }
                }
            }
        }

        stage('Approval') {
            steps {
                input message: 'Approve infrastructure changes?', ok: 'Apply'
            }
        }

        stage('Infrastructure Terraform Apply') {
            steps {
                dir('terraform/infrastructure') {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-key'
                    ]]) {
                        sh 'terraform apply -auto-approve tfplan'
                    }
                }
            }
        }
        
        stage('Capture Output') {
            steps {
                dir('terraform/infrastructure') {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-key'
                    ]]) {
                        script {
                            def instanceIP = sh(
                                script: 'terraform output -raw instance_public_ip',
                                returnStdout: true
                            ).trim()
                            
                            echo "Streamlit application deployed at: http://${instanceIP}:8501"
                            
                            // Archive the IP for future stages
                            writeFile file: 'instance_ip.txt', text: instanceIP
                            archiveArtifacts artifacts: 'instance_ip.txt', fingerprint: true
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Infrastructure deployed successfully!'
        }
        failure {
            echo 'Infrastructure deployment failed.'
        }
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: 'terraform/infrastructure/keys/**', type: 'INCLUDE']])
        }
    }
}