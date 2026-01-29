from pathlib import Path

# checkpoint - guardar numero, offset em bytes

def process_jsonl_incremental(jsonl_path, checkpoint_path):
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Arquivo JSON não existe")


    offset = read_checkpoint(checkpoint_path)


    with jsonl_path.open('rb') as f:
        f.seek(offset) #posicao do cursor 

        while True:
            line_bytes = f.readline()
            if not line_bytes:
                break # se entrar esta vazio ou fim da linha
            
            next_offset = f.tell()
            
    



def read_checkpoint(checkpoint_path):
    if not checkpoint_path.exists():
        checkpoint_path.write_text("0", encoding='utf-8')
        return 0

    return int(checkpoint_path.read_text(encoding='uft-8'))


    





        


a = Path('bronze/bronze_flights/raw.json')
teste = process_jsonl_incremental(a, a)