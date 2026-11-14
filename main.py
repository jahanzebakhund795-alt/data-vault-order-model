"""Data Vault Order Model. Synthetic portfolio demonstration."""
import hashlib
import json

def key(*parts):
    return hashlib.sha256(json.dumps(parts,separators=(',',':')).encode()).hexdigest()

def run(data):
    customers, orders, links, satellites, latest = {}, {}, {}, [], {}
    for row in sorted(data['records'],key=lambda r:r['loaded_at']):
        customer, order = key('customer',row['customer']), key('order',row['order'])
        customers[customer] = row['customer']
        orders[order] = row['order']
        links[key(customer,order)] = {'customer_hk':customer,'order_hk':order}
        difference = key(row['status'])
        if latest.get(order) != difference:
            satellites.append({'order_hk':order,'hashdiff':difference,
                               'status':row['status'],'loaded_at':row['loaded_at']})
            latest[order] = difference
    return {'customer_hubs':customers,'order_hubs':orders,'links':links,'satellites':satellites}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
