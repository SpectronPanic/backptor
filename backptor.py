#!/usr/bin/env python3.5
# -*- coding: utf-8 -*


import subprocess
from datetime import date, timedelta
import logging
import logging.config
from configparser import ConfigParser
import os

__author__ = 'SpectronPanic'
__copyright__ = 'Copyright 2015'
__credits__ = ['SpectronPanic']
__license__ = 'Open Source'
__version__ = '1.0.0'
__maintainer__ = 'SpectronPanic, KernelPanic'
__email__ = 'fj.leite@yahoo.com, kernelpanic2015@gmail.com'
__status__ = 'Development'

cfg_file = 'cfg/config.ini'
logging.config.fileConfig(cfg_file)  # configura o log do sistema
cfg = ConfigParser()
cfg.read(cfg_file)

# diretório de saída
origem = cfg.get('config', 'origem')
# diretório de destino
destino = cfg.get('config', 'destino')
# nome que vem antes da data atual inclusa no final do nome do arquivo
pre_nome = cfg.get('config', 'pre_nome')
# quantia de dias anteriores a data atual a excluir um backup antigo
delete_days = cfg.getint('config', 'delete_days')
# data atual
data_atual = date.today()


def backup_pack():  # função que cria um arquivo compactado adicionando a data atual ao seu nome
    data_atual_formatada = data_atual.strftime('%d%m%Y')
    filename = pre_nome+str(data_atual_formatada)+'.tar'
    pack = subprocess.Popen(['tar', '--overwrite', '-Jcf', destino+filename, origem], stdout=subprocess.PIPE)
    try:
        if pack.wait() == 0:
            logging.info("backup_pack: Backup feito com sucesso!; %s", filename)
        else:
            logging.error("backup_pack: backup_pack = Error %s", pack.wait())
    except Exception as e:
        logging.error("backup_pack: erro: %s", e)


def backup_antigo():  # função que verifica e apaga um backup muito antigo caso esse exista
    data_atual_formatada = data_atual.strftime('%d%m%Y')
    data_antiga = data_atual - timedelta(days=delete_days)
    data_antiga = data_antiga.strftime('%d%m%Y')
    filename_old = 'e2e_'+str(data_antiga)+'.tar'
    patch_oldfile = destino + filename_old
    try:
        if os.path.exists(patch_oldfile):
            pack = subprocess.Popen(['rm', '-rf', patch_oldfile])
            if pack.wait() == 0:
                logging.info("backup_antigo: Backup antigo apagado com sucesso!; %s", filename_old)
        else:
            logging.info("backup_antigo: Backup antigo não existente!")
    except Exception as e:
        logging.error("backup_antigo: erro: %s", data_atual_formatada, e)


backup_pack()
backup_antigo()
