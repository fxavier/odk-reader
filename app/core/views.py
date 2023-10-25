from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import boto3
from .models import *  # Im

load_dotenv()

# Initialize boto3 client for S3
s3 = boto3.client('s3', 
                  aws_access_key_id= os.getenv('AWS_ACCESS_KEY'),
                  aws_secret_access_key= os.getenv('AWS_SECRET_KEY')
                  )

def upload_image_to_s3(image_name, directory_path):
    if not image_name:
        return None

    image_path = os.path.join(directory_path, image_name)
    with open(image_path, 'rb') as image_file:
        s3.upload_fileobj(image_file, os.getenv('S3_BUCKET_NAME'), image_name)
    return f"https://{os.getenv('S3_BUCKET_NAME')}.s3.amazonaws.com/{image_name}"


def process_xml_files_and_upload_to_db():
    print("Processing XML files...")
    directory_path = "C:\Docs\consolidated"
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory_path, filename))
            root = tree.getroot()

            # Generic function to get text from an element
            def get_text(element_name, parent_element=root, default=None):
                elem = parent_element.find(element_name)
                return elem.text if elem is not None else default

            # Extracting data for main Inquerito model
            data_inquerito = get_text('data_inquerito')
            hora_inquerito = get_text('hora_inquerito')
            observacoes = get_text('observacao')
            meta_instanceID = get_text('meta/instanceID')
            if data_inquerito and hora_inquerito:
                inquerito = Inquerito(
                    data_inquerito=data_inquerito,
                    hora_inquerito=hora_inquerito,
                    observacoes=observacoes,
                    meta_instanceID=meta_instanceID
                    )
                inquerito.save()
            else:
                continue  # Skip the rest of this loop iteration if essential data is missing

            # Processing IdentificacaoAggFamiliar section
            agg_familiar_data = root.find('identificacao_agg_familiar')
            if agg_familiar_data:
                tipo_impacto = get_text('tipo_impacto', agg_familiar_data)
                nome_proprietario = get_text('nome_proprietario', agg_familiar_data)
                codigo_familia = get_text('codigo_familia', agg_familiar_data)
                data_nascimento = get_text('data_nascimento', agg_familiar_data)
                celular = get_text('celular', agg_familiar_data)
                foto_proprietario = upload_image_to_s3(get_text('foto_proprietario', agg_familiar_data), directory_path)
                casado = get_text('casado', agg_familiar_data)
                nome_conjugue = get_text('nome_conjugue', agg_familiar_data)
                data_nasciment_conjugue = get_text('data_nasciment_conjugue', agg_familiar_data)
                foto_conjugue = upload_image_to_s3(get_text('foto_conjugue', agg_familiar_data), directory_path)
                nome_inquiridor = get_text('nome_inquiridor', agg_familiar_data)
                coordenadas_casa = get_text('coordenadas_casa', agg_familiar_data)
                agg_familiar = IdentificacaoAggFamiliar(
                    inquerito=inquerito,
                    tipo_impacto=tipo_impacto,
                    nome_proprietario=nome_proprietario,
                    codigo_familia=codigo_familia,
                    data_nascimento=data_nascimento,
                    celular=celular,
                    foto_proprietario=foto_proprietario,
                    casado=casado,
                    nome_conjugue=nome_conjugue,
                    data_nasciment_conjugue=data_nasciment_conjugue,
                    foto_conjugue=foto_conjugue,
                    nome_inquiridor=nome_inquiridor,
                    coordenadas_casa=coordenadas_casa
                )
                agg_familiar.save()

            # Processing PropriedadeDaCasa section
            propriedade_data = root.find('propriedade_da_casa')
            if propriedade_data:
                proprietario_casa = get_text('proprietario_casa', propriedade_data)
                tipo_doc = get_text('tipo_doc', propriedade_data)
                outro_tipo_doc = get_text('outro_tipo_doc', propriedade_data)
                foto_documento = upload_image_to_s3(get_text('foto_documento', propriedade_data), directory_path)
                bairro = get_text('bairro', propriedade_data)
                outro_bairro = get_text('outro_bairro', propriedade_data)
                quarteirao_localizada_familia = get_text('quarteirao_localizada_familia', propriedade_data)
                rua_localizada_familia = get_text('rua_localizada_familia', propriedade_data)
                numero_casa_familia = get_text('numero_casa_familia', propriedade_data)
                referencia_casa = get_text('referencia_casa', propriedade_data)

                propriedade = PropriedadeDaCasa(
                    inquerito=inquerito, 
                    proprietario_casa=proprietario_casa, 
                    tipo_doc=tipo_doc,
                    outro_tipo_doc=outro_tipo_doc,
                    foto_documento=foto_documento,
                    bairro=bairro,
                    outro_bairro=outro_bairro,
                    quarteirao_localizada_familia=quarteirao_localizada_familia,
                    rua_localizada_familia=rua_localizada_familia,
                    numero_casa_familia=numero_casa_familia,
                    referencia_casa=referencia_casa
                )
                propriedade.save()


            # Processing CaracteristicasAggFamiliar section
            caracteristicas_data = root.find('caracteristicas_agg_familiar')
            if caracteristicas_data:
                lingua_materna = get_text('lingua_materna', caracteristicas_data)
                outra_lingua = get_text('outra_lingua', caracteristicas_data)
                numero_de_pessoas_na_familia = get_text('numero_de_pessoas_na_familia', caracteristicas_data)
                if numero_de_pessoas_na_familia:
                    numero_de_pessoas_na_familia = int(numero_de_pessoas_na_familia)
                membros_familia_count = get_text('membros_familia_count', caracteristicas_data)
                if membros_familia_count:
                    membros_familia_count = int(membros_familia_count)
                tempo_a_familia_vive_no_talhao = get_text('tempo_a_familia_vive_no_talhao', caracteristicas_data)
                numero_familias_talhao_terreno = get_text('numero_familias_talhao_terreno', caracteristicas_data)
                numero_mulheres_chefe_da_familia_tem = get_text('numero_mulheres_chefe_da_familia_tem', caracteristicas_data)
                
                caracteristicas = CaracteristicasAggFamiliar(
                    inquerito=inquerito, 
                    lingua_materna=lingua_materna, 
                    outra_lingua=outra_lingua,
                    numero_de_pessoas_na_familia=numero_de_pessoas_na_familia,
                    membros_familia_count=membros_familia_count,
                    tempo_a_familia_vive_no_talhao=tempo_a_familia_vive_no_talhao,
                    numero_familias_talhao_terreno=numero_familias_talhao_terreno,
                    numero_mulheres_chefe_da_familia_tem=numero_mulheres_chefe_da_familia_tem
                )
                caracteristicas.save()

                # For sub-sections, like membros_familia within CaracteristicasAggFamiliar:
                for membro_data in caracteristicas_data.findall('membros_familia'):
                    nome = get_text('nome', membro_data)
                    genero_membro_familia = get_text('genero_membro_familia', membro_data)
                    opcao_idade = get_text('opcao_idade', membro_data)
                    idade_anos = get_text('idade_anos', membro_data)
                    if idade_anos:
                        idade_anos = int(idade_anos)
                    estado_civil = get_text('estado_civil', membro_data)
                    ocupacao = get_text('ocupacao', membro_data)
                    grau_parentesco_com_chefe_familia = get_text('grau_parentesco_com_chefe_familia', membro_data)
                    nivel_educacao = get_text('nivel_educacao', membro_data)
                    doenca_cronica = get_text('doenca_cronica', membro_data)
                    tipo_doenca_cronica = get_text('tipo_doenca_cronica', membro_data)
                    outro_tipo_doenca_cronica = get_text('outro_tipo_doenca_cronica', membro_data)
                    deficiencia_fisica_mental = get_text('deficiencia_fisica_mental', membro_data)

                    membro = MembroFamilia(
                        caracteristicas_agg_familiar=caracteristicas,
                        nome=nome,
                        genero_membro_familia=genero_membro_familia,
                        opcao_idade=opcao_idade,
                        idade_anos=idade_anos,
                        estado_civil=estado_civil,
                        ocupacao=ocupacao,
                        grau_parentesco_com_chefe_familia=grau_parentesco_com_chefe_familia,
                        nivel_educacao=nivel_educacao,
                        doenca_cronica=doenca_cronica,
                        tipo_doenca_cronica=tipo_doenca_cronica,
                        outro_tipo_doenca_cronica=outro_tipo_doenca_cronica,
                        deficiencia_fisica_mental=deficiencia_fisica_mental
                    )
                    membro.save()

            # Processing PatrimonioRendaConsumo section
            patrimonio_data = root.find('patrimonio_renda_consumo')
            if patrimonio_data:
                familia_possui_bens = get_text('familia_possui_bens', patrimonio_data)
                if familia_possui_bens:
                    patrimonio = PatrimonioRendaConsumo(
                        inquerito=inquerito,
                        familia_possui_bens=familia_possui_bens
                    )
                    patrimonio.save()

            # Processing PatrimonioRendaConsumo section
            patrimonio_data = root.find('patrimonio_renda_consumo')
            if patrimonio_data:
                familia_possui_bens = get_text('familia_possui_bens', patrimonio_data)
                numero_de_fontes_de_renda = get_text('numero_de_fontes_de_renda', patrimonio_data)
                if numero_de_fontes_de_renda:
                    numero_de_fontes_de_renda = int(numero_de_fontes_de_renda)
                principais_fontes_de_rendas_count = get_text('principais_fontes_de_rendas_count', patrimonio_data)
                if principais_fontes_de_rendas_count:
                    principais_fontes_de_rendas_count = int(principais_fontes_de_rendas_count)
                principais_fontes_de_rendas = get_text('principais_fontes_de_rendas', patrimonio_data)
                renda_media_mensal = get_text('renda_media_mensal', patrimonio_data)

                patrimonio = PatrimonioRendaConsumo(
                    inquerito=inquerito,
                    familia_possui_bens=familia_possui_bens,
                    numero_de_fontes_de_renda=numero_de_fontes_de_renda,
                    principais_fontes_de_rendas_count=principais_fontes_de_rendas_count,
                    principais_fontes_de_rendas=principais_fontes_de_rendas,
                    renda_media_mensal=renda_media_mensal
                )
                patrimonio.save()

            # Processing ServicosPublicos section
            servicos_publicos_data = root.find('servicos_publicos')
            if servicos_publicos_data:
                donde_busca_agua_para_uso_na_familia = get_text('donde_busca_agua_para_uso_na_familia', servicos_publicos_data)
                outro = get_text('outro', servicos_publicos_data)
                quantidade_bidoes = get_text('quantidade_bidoes', servicos_publicos_data)
                if quantidade_bidoes:
                    quantidade_bidoes = int(quantidade_bidoes)
                tipo_tratamento_agua = get_text('tipo_tratamento_agua', servicos_publicos_data)
                tempo_levado_para_chegar_local_agua = get_text('tempo_levado_para_chegar_local_agua', servicos_publicos_data)
                como_vai_buscar_agua = get_text('como_vai_buscar_agua', servicos_publicos_data)
                quem_vai_buscar_agua = get_text('quem_vai_buscar_agua', servicos_publicos_data)
                principal_fonte_energia_usada_para_cozinha = get_text('principal_fonte_energia_usada_para_cozinha', servicos_publicos_data)
                tempo_para_chegar_local_compra_fonte_energia = get_text('tempo_para_chegar_local_compra_fonte_energia', servicos_publicos_data)
                meio_transporte_para_local_recolha_energia = get_text('meio_transporte_para_local_recolha_energia', servicos_publicos_data)
                fonte_energia_para_iluminacao_casa = get_text('fonte_energia_para_iluminacao_casa', servicos_publicos_data)
                outra_fonte_para_iluminacao_casa = get_text('outra_fonte_para_iluminacao_casa', servicos_publicos_data)
                
                
                servicos_publicos = ServicosPublicos(
                    inquerito=inquerito,
                    donde_busca_agua_para_uso_na_familia=donde_busca_agua_para_uso_na_familia,
                    outro=outro,
                    quantidade_bidoes=quantidade_bidoes,
                    tipo_tratamento_agua=tipo_tratamento_agua,
                    tempo_levado_para_chegar_local_agua=tempo_levado_para_chegar_local_agua,
                    como_vai_buscar_agua=como_vai_buscar_agua,
                    quem_vai_buscar_agua=quem_vai_buscar_agua,
                    principal_fonte_energia_usada_para_cozinha=principal_fonte_energia_usada_para_cozinha,
                    tempo_para_chegar_local_compra_fonte_energia=tempo_para_chegar_local_compra_fonte_energia,
                    meio_transporte_para_local_recolha_energia=meio_transporte_para_local_recolha_energia,
                    fonte_energia_para_iluminacao_casa=fonte_energia_para_iluminacao_casa,
                    outra_fonte_para_iluminacao_casa=outra_fonte_para_iluminacao_casa,
                   
                )           
                servicos_publicos.save()

            # Processing EducacaoSaude section
            educacao_saude_data = root.find('educacao_saude')
            if educacao_saude_data:
                existe_escola_no_bairro = get_text('existe_escola_no_bairro', educacao_saude_data)
                tem_membro_estudante = get_text('tem_membro_estudante', educacao_saude_data)
                quantos_membros = get_text('quantos_membros', educacao_saude_data)
                if quantos_membros:
                    quantos_membros = int(quantos_membros)
                escola_que_frequentam_criancas_familia_count = get_text('escola_que_frequentam_criancas_familia_count', educacao_saude_data)
                if escola_que_frequentam_criancas_familia_count:
                    escola_que_frequentam_criancas_familia_count = int(escola_que_frequentam_criancas_familia_count)
                existe_centro_saude = get_text('existe_centro_saude', educacao_saude_data)
                nome_centro_saude = get_text('nome_centro_saude', educacao_saude_data)
                onde_procura_tratamento = get_text('onde_procura_tratamento', educacao_saude_data)
                tempo_para_chegar_local_tratamento = get_text('tempo_para_chegar_local_tratamento', educacao_saude_data)
                doencas_familia_sofre_mais = get_text('doencas_familia_sofre_mais', educacao_saude_data)

                educacao_saude = EducacaoSaude(
                    inquerito=inquerito,
                    existe_escola_no_bairro=existe_escola_no_bairro,
                    tem_membro_estudante=tem_membro_estudante,
                    quantos_membros=quantos_membros,
                    escola_que_frequentam_criancas_familia_count=escola_que_frequentam_criancas_familia_count,
                    existe_centro_saude=existe_centro_saude,
                    nome_centro_saude=nome_centro_saude,
                    onde_procura_tratamento=onde_procura_tratamento,
                    tempo_para_chegar_local_tratamento=tempo_para_chegar_local_tratamento,
                    doencas_familia_sofre_mais=doencas_familia_sofre_mais
                )
                educacao_saude.save()

            # Processing EstruturasHabitacionais section
            estruturas_habitacionais_data = root.find('estruturas_habitacionais')
            if estruturas_habitacionais_data:
                a_casa_que_vives_e = get_text('a_casa_que_vives_e', estruturas_habitacionais_data)
                comprimento_talhao = get_text('comprimento_talhao', estruturas_habitacionais_data)
                if comprimento_talhao:
                    comprimento_talhao = float(comprimento_talhao)
                largura_talhao = get_text('largura_talhao', estruturas_habitacionais_data)
                if largura_talhao:
                    largura_talhao = float(largura_talhao)
                de_que_material_feita_vedacao_talhao = get_text('de_que_material_feita_vedacao_talhao', estruturas_habitacionais_data)
                outro_material_vedacao = get_text('outro_material_vedacao', estruturas_habitacionais_data)
                quantas_estruturas_tem_o_talhao = get_text('quantas_estruturas_tem_o_talhao', estruturas_habitacionais_data)
                if quantas_estruturas_tem_o_talhao:
                    quantas_estruturas_tem_o_talhao = int(quantas_estruturas_tem_o_talhao)
                estruturas_talhaos_count = get_text('estruturas_talhaos_count', estruturas_habitacionais_data)
                if estruturas_talhaos_count:
                    estruturas_talhaos_count = int(estruturas_talhaos_count)
                quanto_tempo_tem_casa_principal = get_text('quanto_tempo_tem_casa_principal', estruturas_habitacionais_data)
                familia_tem_duat_talhao = get_text('familia_tem_duat_talhao', estruturas_habitacionais_data)
                familia_possui_outra_estrutura_fora_deste_talhao = get_text('familia_possui_outra_estrutura_fora_deste_talhao', estruturas_habitacionais_data)
                
                estruturas_habitacionais = EstruturasHabitacionais(
                    inquerito=inquerito,
                    a_casa_que_vives_e=a_casa_que_vives_e,
                    comprimento_talhao=comprimento_talhao,
                    largura_talhao=largura_talhao,
                    de_que_material_feita_vedacao_talhao=de_que_material_feita_vedacao_talhao,
                    outro_material_vedacao=outro_material_vedacao,
                    quantas_estruturas_tem_o_talhao=quantas_estruturas_tem_o_talhao,
                    estruturas_talhaos_count=estruturas_talhaos_count,
                    quanto_tempo_tem_casa_principal=quanto_tempo_tem_casa_principal,
                    familia_tem_duat_talhao=familia_tem_duat_talhao,
                    familia_possui_outra_estrutura_fora_deste_talhao=familia_possui_outra_estrutura_fora_deste_talhao
                )
                estruturas_habitacionais.save()

            
            # Processing EstruturasTalhaos section
            estruturas_talhaos_data = root.find('estruturas_talhaos')
            if estruturas_talhaos_data:
                estruturas_talhao = get_text('estruturas_talhao', estruturas_talhaos_data)
                estrutura_sera_afectada = get_text('estrutura_sera_afectada', estruturas_talhaos_data)
                codigo_estrutura_afectada = get_text('codigo_estrutura_afectada', estruturas_talhaos_data)
                numero_divisoes = get_text('numero_divisoes', estruturas_talhaos_data)
                if numero_divisoes:
                    numero_divisoes = int(numero_divisoes)
                nivel_afectacao_estrutura = get_text('nivel_afectacao_estrutura', estruturas_talhaos_data)
                comprimento = get_text('comprimento', estruturas_talhaos_data)
                if comprimento:
                    comprimento = float(comprimento)
                largura = get_text('largura', estruturas_talhaos_data)
                if largura:
                    largura = float(largura)
                material_cobertura_estruturas = get_text('material_cobertura_estruturas', estruturas_talhaos_data)
                outro_material_tecto = get_text('outro_material_tecto', estruturas_talhaos_data)
                material_das_paredes = get_text('material_das_paredes', estruturas_talhaos_data)
                material_de_soalho_das_estruturas = get_text('material_de_soalho_das_estruturas', estruturas_talhaos_data)
                outro_material_soalho = get_text('outro_material_soalho', estruturas_talhaos_data)
                foto_esboco = upload_image_to_s3(get_text('foto_esboco', estruturas_talhaos_data), directory_path)
                estruturas_talhaos = EstruturasTalhaos(
                    estruturas_habitacionais=estruturas_habitacionais,  # Assuming you've created an instance of EstruturasHabitacionais before this
                    estruturas_talhao=estruturas_talhao,
                    estrutura_sera_afectada=estrutura_sera_afectada,
                    codigo_estrutura_afectada=codigo_estrutura_afectada,
                    numero_divisoes=numero_divisoes,
                    nivel_afectacao_estrutura=nivel_afectacao_estrutura,
                    comprimento=comprimento,
                    largura=largura,
                    material_cobertura_estruturas=material_cobertura_estruturas,
                    outro_material_tecto=outro_material_tecto,
                    material_das_paredes=material_das_paredes,
                    material_de_soalho_das_estruturas=material_de_soalho_das_estruturas,
                    outro_material_soalho=outro_material_soalho,
                    foto_esboco=foto_esboco
                
                )
                estruturas_talhaos.save()

            

            # Processing ReligiaoELocaisSagrados section
            religiao_e_locais_sagrados_data = root.find('religiao_e_locais_sagrados')
            if religiao_e_locais_sagrados_data:
                religiao = get_text('religiao', religiao_e_locais_sagrados_data)
                tempo_chegar_igreja = get_text('tempo_chegar_igreja', religiao_e_locais_sagrados_data)
                onde_enterra_entequeridos = get_text('onde_enterra_entequeridos', religiao_e_locais_sagrados_data)
                familia_tem_campas = get_text('familia_tem_campas', religiao_e_locais_sagrados_data)
                frequencia_com_que_vai_cemiterio = get_text('frequencia_com_que_vai_cemiterio', religiao_e_locais_sagrados_data)

                religiao_e_locais_sagrados = ReligiaoELocaisSagrados(
                    inquerito=inquerito,
                    religiao=religiao,
                    tempo_chegar_igreja=tempo_chegar_igreja,
                    onde_enterra_entequeridos=onde_enterra_entequeridos,
                    familia_tem_campas=familia_tem_campas,
                    frequencia_com_que_vai_cemiterio=frequencia_com_que_vai_cemiterio
                )
                religiao_e_locais_sagrados.save()

            # Processing Pecuaria section
            pecuaria_data = root.find('pecuaria')
            if pecuaria_data:
                familia_cria_animais = get_text('familia_cria_animais', pecuaria_data)
                familia_possui_arvores = get_text('familia_possui_arvores', pecuaria_data)
                if familia_cria_animais:
                    pecuaria = Pecuaria(
                        inquerito=inquerito,
                        familia_cria_animais=familia_cria_animais,
                        familia_possui_arvores=familia_possui_arvores
                    )
                    pecuaria.save()

            
            # Processing ArvoreFruta section
            arvore_fruta_data = root.find('arvore_fruta')
            if arvore_fruta_data:
                arvore_de_frutas = get_text('arvore_de_frutas', arvore_fruta_data)
                outra_arvore_de_fruta = get_text('outra_arvore_de_fruta', arvore_fruta_data)
                quantidade_arvores = get_text('quantidade_arvores', arvore_fruta_data)
                idade_arvores = get_text('idade_arvores', arvore_fruta_data)
                tempo_producao_frutas = get_text('tempo_producao_frutas', arvore_fruta_data)

                if quantidade_arvores:
                    quantidade_arvores = int(quantidade_arvores)
                if idade_arvores:
                    idade_arvores = int(idade_arvores)
                if tempo_producao_frutas:
                    tempo_producao_frutas = float(tempo_producao_frutas)

                if arvore_de_frutas:
                    arvore_fruta = ArvoreFruta(
                        pecuaria=pecuaria,  # Assuming pecuaria object has been created and is available
                        arvore_de_frutas=arvore_de_frutas,
                        outra_arvore_de_fruta=outra_arvore_de_fruta,
                        quantidade_arvores=quantidade_arvores,
                        idade_arvores=idade_arvores,
                        tempo_producao_frutas=tempo_producao_frutas
                    )
                    arvore_fruta.save()

            # Processing ResolucaoConflitos section
            resolucao_conflitos_data = root.find('resolucao_conflitos')
            if resolucao_conflitos_data:
                a_quem_recorre_em_caso_de_conflitos = get_text('a_quem_recorre_em_caso_de_conflitos', resolucao_conflitos_data)
                metodo_para_receber_informacao = get_text('metodo_para_receber_informacao', resolucao_conflitos_data)
                metodo_para_dar_informacao = get_text('metodo_para_dar_informacao', resolucao_conflitos_data)

                if a_quem_recorre_em_caso_de_conflitos or metodo_para_receber_informacao or metodo_para_dar_informacao:
                    resolucao_conflitos = ResolucaoConflitos(
                        inquerito=inquerito,
                        a_quem_recorre_em_caso_de_conflitos=a_quem_recorre_em_caso_de_conflitos,
                        metodo_para_receber_informacao=metodo_para_receber_informacao,
                        metodo_para_dar_informacao=metodo_para_dar_informacao
                    )
                    resolucao_conflitos.save()


            # Processing ExpectativasTratamento section
            expectativas_tratamento_data = root.find('expectativas_tratamento')
            if expectativas_tratamento_data:
                ao_sair_do_lugar_o_que_espera_como_compensacao = get_text('ao_sair_do_lugar_o_que_espera_como_compensacao', expectativas_tratamento_data)
                outra_compensacao_esperada = get_text('outra_compensacao_esperada', expectativas_tratamento_data)
                onde_gostaria_de_ser_reassentado = get_text('onde_gostaria_de_ser_reassentado', expectativas_tratamento_data)

                # Processing images for foto_esboco_estrutura
                foto_esboco_estrutura_name = upload_image_to_s3(get_text('foto_esboco_estrutura', expectativas_tratamento_data), directory_path)
                
                # Processing images for termo_consentimento
                termo_consentimento_name = upload_image_to_s3(get_text('termo_consentimento', expectativas_tratamento_data), directory_path)
         

                if ao_sair_do_lugar_o_que_espera_como_compensacao or onde_gostaria_de_ser_reassentado:
                    expectativas_tratamento = ExpectativasTratamento(
                        inquerito=inquerito,
                        ao_sair_do_lugar_o_que_espera_como_compensacao=ao_sair_do_lugar_o_que_espera_como_compensacao,
                        outra_compensacao_esperada=outra_compensacao_esperada,
                        onde_gostaria_de_ser_reassentado=onde_gostaria_de_ser_reassentado,
                        foto_esboco_estrutura=foto_esboco_estrutura_name if foto_esboco_estrutura_name else None,
                        termo_consentimento=termo_consentimento_name if termo_consentimento_name else None
                    )
                    expectativas_tratamento.save()







@csrf_exempt  # This is to exempt the view from CSRF protection; use it only if necessary
def index(request):
    process_xml_files_and_upload_to_db()

    return JsonResponse({"status": "success", "message": "XML files processed successfully."})
   