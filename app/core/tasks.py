import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import boto3
from celery import shared_task
from .models import *  # Import all your Django models

# Load environment variables from .env file
load_dotenv()

# Initialize boto3 client for S3
s3 = boto3.client('s3', 
                  aws_access_key_id= os.getenv('AWS_ACCESS_KEY'),
                  aws_secret_access_key= os.getenv('AWS_SECRET_KEY')
                  )

@shared_task(acks_late=True)
def process_xml_files_and_upload_to_db():
    print("Processing XML files...")
    directory_path = "C:\Docs\consolidated"
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory_path, filename))
            root = tree.getroot()

            # Extracting data for main Inquerito model
            data_inquerito = root.find('data_inquerito').text
            hora_inquerito = root.find('hora_inquerito').text

            inquerito = Inquerito(data_inquerito=data_inquerito, hora_inquerito=hora_inquerito)
            inquerito.save()

            # Processing images
            image_name = root.find('foto_proprietario').text
            if image_name:
                image_path = os.path.join(directory_path, image_name)
                with open(image_path, 'rb') as image_file:
                    s3.upload_fileobj(image_file, os.getenv('S3_BUCKET_NAME'), image_name)
                    image_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.amazonaws.com/{image_name}"
                    inquerito.foto_proprietario_url = image_url
                    inquerito.save()

            # Processing IdentificacaoAggFamiliar section
            agg_familiar_data = root.find('identificacao_agg_familiar')
            tipo_impacto = agg_familiar_data.find('tipo_impacto').text
            nome_proprietario = agg_familiar_data.find('nome_proprietario').text

            agg_familiar = IdentificacaoAggFamiliar(
                inquerito=inquerito, 
                tipo_impacto=tipo_impacto, 
                nome_proprietario=nome_proprietario
            )
            agg_familiar.save()
            
             # Processing PropriedadeDaCasa section
            propriedade_data = root.find('propriedade_da_casa')
            proprietario_casa = propriedade_data.find('proprietario_casa').text
            tipo_doc = propriedade_data.find('tipo_doc').text
            bairro = propriedade_data.find('bairro').text

            propriedade = PropriedadeDaCasa(
                inquerito=inquerito, 
                proprietario_casa=proprietario_casa, 
                tipo_doc=tipo_doc,
                bairro=bairro
            )
            propriedade.save()

            # Processing CaracteristicasAggFamiliar section
            caracteristicas_data = root.find('caracteristicas_agg_familiar')
            lingua_materna = caracteristicas_data.find('lingua_materna').text
            numero_de_pessoas_na_familia = int(caracteristicas_data.find('numero_de_pessoas_na_familia').text)

            caracteristicas = CaracteristicasAggFamiliar(
                inquerito=inquerito, 
                lingua_materna=lingua_materna, 
                numero_de_pessoas_na_familia=numero_de_pessoas_na_familia
            )
            caracteristicas.save()

            # For sub-sections, like membros_familia within CaracteristicasAggFamiliar:
            for membro_data in caracteristicas_data.findall('membros_familia'):
                nome = membro_data.find('nome').text
                genero_membro_familia = membro_data.find('genero_membro_familia').text

                membro = MembroFamilia(
                    caracteristicas=caracteristicas,
                    nome=nome,
                    genero_membro_familia=genero_membro_familia
                )
                membro.save()

            # Processing PatrimonioRendaConsumo section
            patrimonio_data = root.find('patrimonio_renda_consumo')
            familia_possui_bens = patrimonio_data.find('familia_possui_bens').text

            patrimonio = PatrimonioRendaConsumo(
                inquerito=inquerito,
                familia_possui_bens=familia_possui_bens
            )
            patrimonio.save()

            # Processing BensFamilia section
            bens_familia_data = root.find('bens_familia')
            if bens_familia_data:  # Check if the section exists
                bens = bens_familia_data.find('bens').text
                
                bens_familia = BensFamilia(
                    inquerito=inquerito,
                    bens=bens
                )
                bens_familia.save()

            # Processing ServicosPublicos section
            servicos_publicos_data = root.find('servicos_publicos')
            if servicos_publicos_data:  # Check if the section exists
                # (Assuming hypothetical fields here; please adjust accordingly)
                agua = servicos_publicos_data.find('agua').text
                eletricidade = servicos_publicos_data.find('eletricidade').text

                servicos_publicos = ServicosPublicos(
                    inquerito=inquerito,
                    agua=agua,
                    eletricidade=eletricidade
                )
                servicos_publicos.save()

            # Processing EducacaoSaude section
            educacao_saude_data = root.find('educacao_saude')
            if educacao_saude_data:  # Check if the section exists
                # (Assuming hypothetical fields here; please adjust accordingly)
                escolaridade = educacao_saude_data.find('escolaridade').text
                acesso_saude = educacao_saude_data.find('acesso_saude').text

                educacao_saude = EducacaoSaude(
                    inquerito=inquerito,
                    escolaridade=escolaridade,
                    acesso_saude=acesso_saude
                )
                educacao_saude.save()

            # Processing ExpectativasTratamento section
            expectativas_tratamento_data = root.find('expectativas_tratamento')
            if expectativas_tratamento_data:  # Check if the section exists
                # (Assuming hypothetical fields here; please adjust accordingly)
                expectativas = expectativas_tratamento_data.find('expectativas').text

                expectativas_tratamento = ExpectativasTratamento(
                    inquerito=inquerito,
                    expectativas=expectativas
                )
                expectativas_tratamento.save()



