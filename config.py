# ─────────────────────────────────────────────
# config.py
# Archivo de configuración global del TFG
# Importar en cada script con: from config import *
# ─────────────────────────────────────────────

from pathlib import Path

# ══════════════════════════════════════════════
# RUTAS
# ══════════════════════════════════════════════

CARPETA_DATOS     = Path(r"C:\Users\nacho\OneDrive\Escritorio\C-MAPSS 2\datos")
CARPETA_NORM      = Path(r"C:\Users\nacho\OneDrive\Escritorio\C-MAPSS 2\normalizados")
CARPETA_VENTANAS  = Path(r"C:\Users\nacho\OneDrive\Escritorio\C-MAPSS 2\ventanas")


# ══════════════════════════════════════════════
# COLUMNAS
# ══════════════════════════════════════════════

COLS_W       = ['alt', 'Mach', 'TRA', 'T2']
COLS_META    = ['unit', 'cycle', 'Fc', 'hs']
COLS_EXCLUIR = COLS_W + COLS_META + ['RUL']


# ══════════════════════════════════════════════
# PARÁMETROS DE VENTANA
# ══════════════════════════════════════════════

VENTANA = 30
PASO    = 25


# ══════════════════════════════════════════════
# PARÁMETROS DE MODELOS
# ══════════════════════════════════════════════

# Random Forest
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH    = 15
RF_RANDOM_STATE = 42

# Deep Learning (para scripts futuros)
DL_BATCH_SIZE   = 64
DL_EPOCHS       = 50
DL_LEARNING_RATE = 0.001


# ══════════════════════════════════════════════
# UNIDADES POR MODO DE FALLO (según PDF)
# ══════════════════════════════════════════════

UNIDADES_HPT     = [2, 5, 10]
UNIDADES_HPT_LPT = [16, 18, 20]
UNIDADES_TEST    = [11, 14, 15]



# ══════════════════════════════════════════════
# PARÁMETROS DEEP LEARNING
# ══════════════════════════════════════════════

# Arquitectura
LSTM_UNITS       = 64
LSTM_LAYERS      = 2
DROPOUT          = 0.2
DENSE_UNITS      = 32

# Entrenamiento
DL_BATCH_SIZE    = 64
DL_EPOCHS        = 50
DL_LEARNING_RATE = 0.001

# Early stopping
ES_PATIENCE      = 10
LR_PATIENCE      = 5
LR_FACTOR        = 0.5
LR_MIN           = 1e-6

# Rutas de modelos guardados
RUTA_MODELO_RF   = Path(r"C:\Users\nacho\OneDrive\Escritorio\UCLM AEROESPACIAL\TFG\CÓDIGOS\modelo_rf.pkl")
RUTA_MODELO_LSTM = Path(r"C:\Users\nacho\OneDrive\Escritorio\UCLM AEROESPACIAL\TFG\CÓDIGOS\modelo_lstm.h5")
RUTA_MODELO_BILSTM  = Path(r"C:\Users\nacho\OneDrive\Escritorio\UCLM AEROESPACIAL\TFG\CÓDIGOS\modelo_bilstm.h5")
RUTA_MODELO_CNNLSTM = Path(r"C:\Users\nacho\OneDrive\Escritorio\UCLM AEROESPACIAL\TFG\CÓDIGOS\modelo_cnnlstm.h5")