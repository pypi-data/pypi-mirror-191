import os, argparse, tarfile, sys, traceback
IS_BUILD_MODE = int(os.environ.get('IS_BUILD_MODE', 0))
if not IS_BUILD_MODE:
    import oss2



__version__='0.0.6'



def upload(args):
    id = args.id
    secret = args.secret
    bucket_name = args.bucket
    local_path = args.local
    object_name = args.object
    endpoint = args.endpoint
    use_tar = args.use_tar
    use_control_signal = args.use_control_signal
    signal_path = args.signal_path
    if not id:
        id = os.environ.get('OSS_ID')
    if not secret:
        secret = os.environ.get('OSS_SECRET')
    if not bucket_name:
        bucket_name = os.environ.get('BUCKET_NAME')
    if not endpoint:
        endpoint = os.environ.get('ENDPOINT')
    
    if use_control_signal:
        with open(signal_path, 'w') as f:
            f.write('0')
    if not os.path.exists(local_path):
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('-1')
        raise FileNotFoundError('Path does not exist')
    elif os.path.isdir(local_path):
        use_tar = True
    if use_tar:
        dirname = os.path.dirname(local_path)
        basename = os.path.basename(local_path)
        basename = basename.split('.')[0]
        tar_name = os.path.join(dirname, f'{basename}.tar.gz')
        tar = tarfile.open(tar_name, 'w:gz') 
        tar.add(local_path)
        tar.close()
        local_path = tar_name
    auth = oss2.Auth(id, secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    try:
        with open(local_path, 'rb') as f:
            bucket.put_object(object_name, f)
        if use_tar:
            os.remove(local_path)
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('1')
    except:
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('-1')
        traceback.print_exc()
        sys.exit(1)



def download(args):
    id = args.id
    secret = args.secret
    bucket_name = args.bucket
    local_path = args.local
    object_name = args.object
    endpoint = args.endpoint
    use_control_signal = args.use_control_signal
    signal_path = args.signal_path

    if not id:
        id = os.environ.get('OSS_ID')
    if not secret:
        secret = os.environ.get('OSS_SECRET')
    if not bucket_name:
        bucket_name = os.environ.get('BUCKET_NAME')
    if not endpoint:
        endpoint = os.environ.get('ENDPOINT')

    try:
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('0')
        auth = oss2.Auth(id, secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        bucket.get_object_to_file(object_name, local_path)
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('1')
    except:
        if use_control_signal:
            with open(signal_path, 'w') as f:
                f.write('-1')
        traceback.print_exc()
        sys.exit(1)



def run():
    parser = argparse.ArgumentParser(description='OSS command line controller')
    subparser = parser.add_subparsers(help='subcommand help')

    up_parser = subparser.add_parser('upload', help='upload file to OSS')
    up_parser.add_argument('--id', type=str, default='', help='Aliyun account id')
    up_parser.add_argument('--secret', type=str, default='', help='Aliyun account secret')
    up_parser.add_argument('--bucket', type=str, default='',help='bucket name')
    up_parser.add_argument('--local', type=str, default='', help='local path')
    up_parser.add_argument('--object', type=str, default='', help='object name')
    up_parser.add_argument('--endpoint', type=str, default='oss-cn-shanghai-internal.aliyuncs.com', help='endpoint')
    up_parser.add_argument('--use_tar', action='store_true', help='compress the give local file')
    up_parser.add_argument('--use_control_signal', action='store_true', help='write control signal in file')
    up_parser.add_argument('--signal_path', type=str, default='/tmp/ossctl-signal', help='path to write signal')
    up_parser.set_defaults(func=upload)

    down_parser = subparser.add_parser('download', help='download file from OSS')
    down_parser.add_argument('--id', type=str, default='', help='Aliyun account id')
    down_parser.add_argument('--secret', type=str, default='', help='Aliyun account secret')
    down_parser.add_argument('--bucket', type=str, default='',help='bucket name')
    down_parser.add_argument('--local', type=str, default='', help='local path')
    down_parser.add_argument('--object', type=str, default='', help='object name')
    down_parser.add_argument('--endpoint', type=str, default='oss-cn-shanghai-internal.aliyuncs.com', help='endpoint')
    down_parser.add_argument('--use_control_signal', action='store_true', help='write control signal in file')
    down_parser.add_argument('--signal_path', type=str, default='/tmp/ossctl-signal', help='path to write signal')
    down_parser.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)



if __name__=='__main__':
    run()