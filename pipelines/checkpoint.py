from pathlib import Path

# checkpoint - guardar numero, offset em bytes

def process_jsonl_incremental(jsonl_path, checkpoint_path):
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Arquivo JSON não encontrado")


    offset = read_checkpoint(checkpoint_path)

    with jsonl_path.open('rb') as f:
        f.seek() #?

def read_checkpoint(checkpoint_path):
    if not checkpoint_path.exists():
        checkpoint_path.write_text("0", encoding='utf-8')
        return 0
    
    return int(checkpoint_path.read_text(encoding='uft-8'))


    





        


a = Path('bronze/bronze_flights/raw.json')
teste = process_jsonl_incremental(a, a)