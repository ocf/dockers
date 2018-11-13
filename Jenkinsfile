pipeline {
  // TODO: Make this cleaner: https://issues.jenkins-ci.org/browse/JENKINS-42643
  triggers {
    upstream(
      upstreamProjects: (env.BRANCH_NAME == 'master' ? 'utils/master' : ''),
      threshold: hudson.model.Result.SUCCESS,
    )

    // Build fresh base images every day at 9 PM.
		// The time of day doesn't really matter on this, but when it builds
		// successfully it triggers other builds which could have failures, so this
    // should probably be during a time when people are awake.
    cron('0 21 * * *')
  }

  agent {
    label 'slave'
  }

  options {
    ansiColor('xterm')
    timeout(time: 1, unit: 'HOURS')
    timestamps()
  }

  stages {
    stage('check-gh-trust') {
      steps {
        checkGitHubAccess()
      }
    }

    stage('attempt-build-images') {
      steps {
        sh 'make build'
      }
    }

    stage('build-without-cache-and-push-images') {
      when {
        branch 'master'
      }
      agent {
        label 'deploy'
      }
      steps {
        sh 'make push'
      }
    }
  }

  post {
    failure {
      emailNotification()
    }
    always {
      node(label: 'slave') {
        ircNotification()
      }
    }
  }
}

// vim: ft=groovy
