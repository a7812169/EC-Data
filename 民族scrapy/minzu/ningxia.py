import os


def get_command(config_file_name):
    config_file = config_file_name + ".yaml"
    command = "scrapy crawl minzu --loglevel WARNING -s config_name=" + config_file_name
    return command


if __name__ == '__main__':
    os.system(get_command("宁夏自治区"))

