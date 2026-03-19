node {
  stage('Preparation') {
    catchError(buildResult: 'SUCCESS') {
      sh 'docker stop sampleapp'
      sh 'docker rm sampleapp'
    }
  }
  stage('Build') {
    build 'BuildAppJob'
  }
  stage('Results') {
    build 'TestAppJob'
  }
}
