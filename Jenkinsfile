pipeline {
  agent any
  stages {
    stage('Tests') {
      parallel {
        stage('Compile') {
          agent {docker {image 'python:3-alpine'}}
          steps {
            sh 'python -m py_compile **.py'
            stash(name: 'compiled-results', includes: '**.py*')
          }
        }
        node {
          stage('SCM') {
            git 'https://github.com/Drentem/LOPFIT.git'
          }
          stage('SonarQube') {
            def scannerHome = tool 'SonarScanner 4.0';
            withSonarQubeEnv('SonarQube') { // If you have configured more than one global server connection, you can specify its name
              sh "${scannerHome}/bin/sonar-scanner"
            }
          }
        }
/*
        stage('SonarQube') {
          steps {
            withSonarQubeEnv('SonarQube') {
              sh ""
            }
          }
        }
*/
      }
    }
    stage('Quality Gate') {
      steps{
        waitForQualityGate abortPipeline: true
      }
    }
  }
}
