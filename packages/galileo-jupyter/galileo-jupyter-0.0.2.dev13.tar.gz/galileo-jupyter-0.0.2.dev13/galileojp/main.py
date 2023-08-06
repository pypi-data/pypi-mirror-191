import logging

from galileojp.k3s import K3SGateway


def main():
    logging.basicConfig()
    gw = K3SGateway.from_env()
    exp_id = '202302041750-d17c'
    print(gw.get_exp_params(exp_id))
    # gw.export(exp_id, '/tmp')

if __name__ == '__main__':
    main()
