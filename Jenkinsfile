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
    //     stage('Build and Tag Openshift Image'){
    //         steps{
    //             openshiftBuild(namespace:'${openshiftProject}', bldCfg: 'job-ad-loaders', showBuildLogs: 'true')
    //             openshiftTag(namespace:'${openshiftProject}', srcStream: 'job-ad-loaders', srcTag: 'latest', destStream: 'job-ad-loaders', destTag:'${buildTag}')
    //         }
    //     }
    //     stage('Change Cronjob Image'){
    //         steps{
    //             sh "oc patch cronjobs/jobtechjobs-loader --type=json -p='[{\"op\":\"replace\", \"path\": \"/spec/jobTemplate/spec/template/spec/containers/0/image\", \"value\":\"docker-registry.default.svc:5000/${openshiftProject}/elastic-importers:${buildTag}\"}]' -n ${openshiftProject}"
    //         }
    //     }
    }
    post {
        success {
            slackSend color: 'good', message: "${GIT_URL} ${GIT_BRANCH} ${GIT_COMMIT} successfully built to ${openshiftProject} build ${buildTag}."
        }
        failure {
            slackSend color: 'bad', message: "${GIT_URL} ${GIT_BRANCH} ${GIT_COMMIT} failed to build to ${openshiftProject} build ${buildTag}."
        }
        unstable {
            slackSend color: 'bad', message: "${GIT_URL} ${GIT_BRANCH} ${GIT_COMMIT} unstable build for ${openshiftProject} build ${buildTag}."
        }
    }
}
