pipeline {
    agent any
    environment {
        scannerHome = tool 'Jobtech_Sokapi_SonarScanner'
        version = "1"
        buildTag = "${version}.${BUILD_NUMBER}"
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
                sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=job_ad_loader -Dsonar.sources=."
                }
            }
        }
        stage('Build Openshift Image'){
            steps{
                openshiftBuild(namespace:'${openshiftProject}', bldCfg: 'job-ad-loaders', showBuildLogs: 'true')
            }
        }
    }
}
