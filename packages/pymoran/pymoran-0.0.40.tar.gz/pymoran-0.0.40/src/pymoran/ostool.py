import os


class FileClass:
    def __init__(self):
        pass

    def exists(self, path: str, type: str = 'dir'):
        '''
        判断文件或目录是否存在
        :param path 完整的文件/目录地址，如：/User/File或/User/File/hello.py
        :param type dir/file，默认dir
        return {bool} True存在，False不存在
        '''
        if (os.path.isdir(path) and type == 'dir') or (os.path.isfile(path) and type == 'file'):
            return os.path.exists(path)
        return False

    def mkdir(self, path: str, name: str):
        '''
        在指定目录创建目录
        :param path 需要创建目录的路径，如：/User/File
        :param name 目录名称
        return {bool} True创建成功，False创建失败，目录已存在
        '''
        path = path+'/'+name
        if self.exists(path) == True:
            return False
        os.mkdir(path+'/'+name)
        return True


    def rmfile(self,path:str):
        '''
        递归删除目录下所有文件及子目录
        :param path 需要删除的目录，如/User/File
        return {bool} True删除成功
        '''
        cfilepath=self.get_dir_filepath(path)
        dirpath=[]
        for cpath in cfilepath:
            if os.path.isdir(cpath):
                # 如果路径为目录，则保存到目录列表
                dirpath.append(cpath)
            if os.path.isfile(cpath):
                # 如果路径为文件，则删除文件
                os.remove(cpath)
        # 循环删除剩下的空目录
        for dpath in dirpath:
            os.rmdir(dpath)
        return True

    def get_dir_filename(self, path: str):
        '''
        获取指定目录下所有子文件名称
        :param path 目录路径
        return {list} 所有子文件名称
        '''
        file_list = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name == '.DS_Store':
                    continue
                file_list.append(name)
        return file_list

    def get_dir_filepath(self, path:str):
        '''
        获取指定目录下所有子文件绝对路径
        :param path 目录路径
        return {list} 所有子文件路径
        '''
        file_list = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name == '.DS_Store':
                    continue
                file_path = os.path.join(root, name).replace('\\', '/')
                file_list.append(file_path)
        return file_list

    def get_abspath(self):
        path = os.path.abspath('.')
        return path


if __name__ == '__main__':
    fileclass = FileClass()
    res=fileclass.get_dir_filepath('/Volumes/Files/待处理图片')
    print(res)
