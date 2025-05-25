if [[ -z $1 ]]; then
	echo "usage: $0 <name> <client_id> <secret> <scope>"
	exit 1
fi

NAME=$1
AZURE_CLIENT_ID=$2
AZURE_CLIENT_SECRET=$3
AZURE_SCOPE=$4

echo ${NAME}:
python3 ./service-principal-token.py
