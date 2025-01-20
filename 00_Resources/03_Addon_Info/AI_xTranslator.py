from lxml import etree
import requests

def translate_with_koboldcpp(text):
    url = "http://localhost:5001/api/v1/generate"
    
    params = {
        "n": 1,
        "max_context_length": 2048,
        "max_length": 700,
        "rep_pen": 1.07,
        "rep_pen_range": 360,
        "rep_pen_slope": 0.7,
        "sampler_order": [6, 0, 1, 3, 4, 2, 5],
        "temperature": 0.2,
        "top_p": 0.92,
        "top_k": 100,
        "top_a": 0,
        "typical": 1,
        "tfs": 1,
        "trim_stop": True,
        "min_p": 0,
        "dynatemp_range": 0, 
        "dynatemp_exponent": 1, 
        "smoothing_factor": 0, 
        "banned_tokens": [], 
        "presence_penalty": 0, 
        "logit_bias": {}, 
        "stop_sequence": ["### Instruction:", "### Response:", "\n"]
    }
    
    data = {
        "prompt": f"### Instruction: Переведи следующий текст на русский язык. Местоимение you всегда переводи в варианте ты, не вы. Твой ответ должен содержать только переведенный текст без дополнительных комментариев:\n{text}\n### Response:",
        **params
    }
    
    response = requests.post(url, json=data)

    print("Ответ от API:", response.json())

    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0].get('text', '')
    else:
        print("Ошибка при переводе:", response.status_code)
    
    return ""

def split_text(text, max_length=2000):
    words = text.split()
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            yield ' '.join(current_chunk)
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        yield ' '.join(current_chunk)

xml_file_path = r"C:\Users\Ananas\file.xml"

with open(xml_file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

parser = etree.XMLParser(recover=True)
root = etree.fromstring(xml_content.encode('utf-8'), parser=parser)
dest_elements = root.findall('.//Dest')

for dest_element in dest_elements:
    if dest_element is not None and dest_element.text:
        text_to_translate = dest_element.text.strip()
        
        translated_text = ""
        
        for chunk in split_text(text_to_translate):
            max_attempts = 7
            attempts = 0
            translated_chunk = ""
            
            while attempts < max_attempts:
                translated_chunk = translate_with_koboldcpp(chunk)
                
                # Проверяем результат на пустую строку или пробел
                if translated_chunk.strip() and translated_chunk.strip() != ' ':
                    break
                
                attempts += 1
                print(f"Попытка {attempts} не удалась, повторяем перевод...")
            
            translated_text += translated_chunk + " "

        dest_element.text = translated_text.strip()

updated_xml = etree.tostring(root, encoding='unicode', pretty_print=True)
print(updated_xml)

output_file_path = r"C:\Users\Ananas\file.xml"
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(updated_xml)
