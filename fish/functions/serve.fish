
function serve -d "Spin up a simple http server"
    if python -c 'import sys; sys.exit(sys.version_info[0] != 3)'
        python -m http.server $argv
    else
        python -m SimpleHTTPServer $argv
    end
end


