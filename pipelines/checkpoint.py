from pathlib import Path
import json
from pipelines.transform_bronze_to_silver import BronzeToSilver
from pipelines.storage import CreateUpdateFiles

# checkpoint - guardar numero, offset em bytes


def process_jsonl_incremental(jsonl_path, checkpoint_path):
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Arquivo JSON não existe")
    
    
    transform = BronzeToSilver()
    storage = CreateUpdateFiles()


    offset = read_checkpoint(checkpoint_path)


    with jsonl_path.open('rb') as f:
        f.seek(offset) #posicao do cursor 

        while True:
            line_bytes = f.readline()
            if not line_bytes:
                break # se entrar esta vazio ou fim da linha
            
            next_offset = f.tell() #checkpoint da linha que acabou de ser lida, ou seja, \n
            
            line_str = line_bytes.decode('utf-8')
            line_str = json.loads(line_str)
            parsed = transform.transform_bronze_to_silver(line_str)

            if parsed:    
                storage.update_silver(**parsed)
                checkpoint_path.write_text(str(next_offset), encoding='utf-8')
            


def read_checkpoint(checkpoint_path):
    if not checkpoint_path.exists():
        checkpoint_path.write_text("0", encoding='utf-8')
        return 0


    return int(checkpoint_path.read_text(encoding='utf-8'))


