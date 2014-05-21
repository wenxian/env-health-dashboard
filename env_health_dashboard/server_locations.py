SFLY_JIRA = "https://bugs.tinyprints.com"

SFLY_CHINA_JENKINS = "http://china.stage.shutterfly.com:2010/"

SFLY_TRE_JENKINS = "http://tre-jenkins.internal.shutterfly.com:8080/"

ALEXANDRIA_SERVER = "http://test-results.internal.shutterfly.com"


def get_server(job_repository):
    if job_repository == "tre-jenkins":
        path_server = SFLY_TRE_JENKINS
    if job_repository == "china":
        path_server = SFLY_CHINA_JENKINS
    return path_server
