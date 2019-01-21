
function serve {
    if [ python -c "import sys; sys.exit(sys.version_info[0] != 3)" ]
    then
        python -m http.server
    else
        python -m SimpleHTTPServer
    fi
}
