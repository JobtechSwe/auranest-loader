pipeline {
    agent any
    environment {
        scannerHome = tool 'Jobtech_Sokapi_SonarScanner'
    }
    stages{
        stage('Checkout code'){
            steps{
                checkout scm: [
                    $class: 'GitSCM'
                ]               
            }
        }
        stage('Code analysis'){
            steps {
                withSonarQubeEnv('Jobtech_SonarQube_Server'){
                sonar.projectKey = 'job-ad-loaders'
                sh "${scannerHome}/bin/sonar-scanner -Dsonar.projecjetKey=sokapi_sonar -Dsonar.sources=."
                }
            }
        }
    }
}
