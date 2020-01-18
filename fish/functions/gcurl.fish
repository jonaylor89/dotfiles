
function gcurl -d "curl with google id"
  set identity (gcloud auth print-identity-token)
  curl -H "Authorization: Bearer $identity" $argv
end
