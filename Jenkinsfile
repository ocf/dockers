if (env.BRANCH_NAME == 'master') {
    properties([
        pipelineTriggers([
            triggers: [
                [
                    $class: 'jenkins.triggers.ReverseBuildTrigger',
                    upstreamProjects: 'utils/master', threshold: hudson.model.Result.SUCCESS,
                ],
            ]
        ]),

        // Build fresh base images every day at 9 PM.
        // The time of day doesn't really matter on this, but when it builds
        // successfully it triggers other builds which could have failures,
        // so this should probably be during a time when people are awake.
        pipelineTriggers([cron('0 21 * * *')]),
    ])
}


try {
    // check out code
    stage name: 'check-out-code'

    node('slave') {
        dir('src') {
            checkout scm
        }
        stash 'src'
    }


    // make sure the containers can build
    stage name: 'attempt-build-images'

    node('slave') {
        unstash 'src'
        dir('src') {
            sh 'make build'
        }
    }


    // deploy to prod
    if (env.BRANCH_NAME == 'master') {
        stage name: 'build-without-cache-and-push-images'
        node('deploy') {
            unstash 'src'
            dir('src') {
                sh 'make push'
            }
        }
    }

} catch (err) {
    def subject = "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - Failure!"
    def message = "${env.JOB_NAME} (#${env.BUILD_NUMBER}) failed: ${env.BUILD_URL}"

    if (env.BRANCH_NAME == 'master') {
        slackSend color: '#FF0000', message: message
        mail to: 'root@ocf.berkeley.edu', subject: subject, body: message
    } else {
        mail to: emailextrecipients([
            [$class: 'CulpritsRecipientProvider'],
            [$class: 'DevelopersRecipientProvider']
        ]), subject: subject, body: message
    }

    throw err
}

// vim: ft=groovy
