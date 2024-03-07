from common import get_data


##########################################################

# Load data

data, prices = get_data()


tags = set([v['tag'] for v in prices])
print(tags)