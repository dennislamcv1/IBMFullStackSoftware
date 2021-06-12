#!/bin/bash

B64_URL=$(ibmcloud resource service-key "Auto-generated service credentials" --output json | jq .[0].credentials.url -j | base64 -w 0)
B64_APIKEY=$(ibmcloud resource service-key "Auto-generated service credentials" --output json | jq .[0].credentials.apikey -j | base64 -w 0)

cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: binding-tone
  namespace: sn-labs-u7mxhi35yba
type: Opaque
data:
  url: $B64_URL
  apikey: $B64_APIKEY
EOF
