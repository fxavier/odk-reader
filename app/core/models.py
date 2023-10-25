from django.db import models

class Inquerito(models.Model):
    data_inquerito = models.DateTimeField(null=True, blank=True)
    hora_inquerito = models.DateTimeField(null=True, blank=True)
    hora_do_termino = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    meta_instanceID = models.TextField(null=True, blank=True)

class IdentificacaoAggFamiliar(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    tipo_impacto = models.CharField(max_length=100, null=True, blank=True)
    nome_proprietario = models.CharField(max_length=200, null=True, blank=True)
    codigo_familia = models.CharField(max_length=255, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    foto_proprietario = models.CharField(max_length=255, null=True, blank=True)
    casado = models.CharField(max_length=10, null=True, blank=True)
    nome_conjugue = models.CharField(max_length=200, null=True, blank=True)
    data_nasciment_conjugue = models.DateField(null=True, blank=True)
    foto_conjugue = models.CharField(max_length=255, null=True, blank=True)
    nome_inquiridor = models.CharField(max_length=100, null=True, blank=True)
    coordenadas_casa = models.CharField(max_length=200, null=True, blank=True)

class IdentificacaoPropNegocio(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    solucao_adoptar = models.CharField(max_length=100, null=True, blank=True)

class PropriedadeDaCasa(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    proprietario_casa = models.CharField(max_length=10, null=True, blank=True)
    tipo_doc = models.CharField(max_length=255, null=True, blank=True)
    outro_tipo_doc = models.CharField(max_length=255, null=True, blank=True)
    foto_documento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    outro_bairro = models.CharField(max_length=100, null=True, blank=True)
    quarteirao_localizada_familia = models.CharField(max_length=255, null=True, blank=True)
    rua_localizada_familia = models.CharField(max_length=255, null=True, blank=True)
    numero_casa_familia = models.CharField(max_length=255, null=True, blank=True)
    referencia_casa = models.CharField(max_length=255, null=True, blank=True)

class CaracteristicasAggFamiliar(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    lingua_materna = models.CharField(max_length=255, null=True, blank=True)
    outra_lingua = models.CharField(max_length=255, null=True, blank=True)
    numero_de_pessoas_na_familia = models.PositiveIntegerField(null=True, blank=True)
    membros_familia_count = models.PositiveIntegerField(null=True, blank=True)
    tempo_a_familia_vive_no_talhao = models.CharField(max_length=100, null=True, blank=True)
    numero_familias_talhao_terreno = models.PositiveIntegerField(null=True, blank=True)
    numero_mulheres_chefe_da_familia_tem = models.CharField(max_length=255, null=True, blank=True)

class MembroFamilia(models.Model):
    caracteristicas_agg_familiar = models.ForeignKey(CaracteristicasAggFamiliar, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True, blank=True)
    genero_membro_familia = models.CharField(max_length=255, null=True, blank=True)
    opcao_idade = models.CharField(max_length=255, null=True, blank=True)
    idade_anos = models.PositiveIntegerField(null=True, blank=True)
    estado_civil = models.CharField(max_length=255, null=True, blank=True)
    ocupacao = models.CharField(max_length=255, null=True, blank=True)
    grau_parentesco_com_chefe_familia = models.CharField(max_length=255, null=True, blank=True)
    nivel_educacao = models.CharField(max_length=255, null=True, blank=True)
    doenca_cronica = models.CharField(max_length=10, null=True, blank=True)
    tipo_doenca_cronica = models.TextField(null=True, blank=True)  # This can be a many-to-many field if you have predefined diseases
    outro_tipo_doenca_cronica = models.CharField(max_length=255, null=True, blank=True)
    deficiencia_fisica_mental = models.CharField(max_length=100, null=True, blank=True)

class PatrimonioRendaConsumo(models.Model):
    inquerito = models.ForeignKey(Inquerito, on_delete=models.CASCADE)
    familia_possui_bens = models.CharField(max_length=10, null=True, blank=True)
    numero_de_fontes_de_renda = models.PositiveIntegerField(null=True, blank=True)
    principais_fontes_de_rendas_count = models.PositiveIntegerField(null=True, blank=True)
    principais_fontes_de_rendas = models.TextField(null=True, blank=True)  # Consider many-to-many if you have predefined sources
    renda_media_mensal = models.CharField(max_length=255, null=True, blank=True)

class BensFamilia(models.Model):
    patrimonio_renda_consumo = models.ForeignKey(PatrimonioRendaConsumo, on_delete=models.CASCADE)
    bens = models.CharField(max_length=100, null=True, blank=True)
    quantidade = models.PositiveIntegerField(null=True, blank=True)

class EstruturasHabitacionais(models.Model):
    inquerito = models.ForeignKey(Inquerito, on_delete=models.CASCADE)
    a_casa_que_vives_e = models.CharField(max_length=255, null=True, blank=True)
    comprimento_talhao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    largura_talhao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    de_que_material_feita_vedacao_talhao = models.CharField(max_length=100, null=True, blank=True)
    outro_material_vedacao = models.CharField(max_length=100, null=True, blank=True)
    quantas_estruturas_tem_o_talhao = models.PositiveIntegerField(null=True, blank=True)
    estruturas_talhaos_count = models.PositiveIntegerField(null=True, blank=True)
    quanto_tempo_tem_casa_principal = models.CharField(max_length=100, null=True, blank=True)
    familia_tem_duat_talhao = models.CharField(max_length=10, null=True, blank=True)
    familia_possui_outra_estrutura_fora_deste_talhao = models.CharField(max_length=10, null=True, blank=True)
    localizacao_outra_estrutura = models.CharField(max_length=100, null=True, blank=True)

class EstruturasTalhaos(models.Model):
    estruturas_habitacionais = models.ForeignKey(EstruturasHabitacionais, on_delete=models.CASCADE)
    estruturas_talhao = models.CharField(max_length=100, null=True, blank=True)
    estrutura_sera_afectada = models.CharField(max_length=10, null=True, blank=True)
    codigo_estrutura_afectada = models.CharField(max_length=255, null=True, blank=True)
    numero_divisoes = models.PositiveIntegerField(null=True, blank=True)
    nivel_afectacao_estrutura = models.CharField(max_length=100, null=True, blank=True)
    comprimento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    largura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    material_cobertura_estruturas = models.CharField(max_length=100, null=True, blank=True)
    outro_material_tecto = models.CharField(max_length=100, null=True, blank=True)
    material_das_paredes = models.CharField(max_length=100, null=True, blank=True)
    material_de_soalho_das_estruturas = models.CharField(max_length=100, null=True, blank=True)
    outro_material_soalho = models.CharField(max_length=100, null=True, blank=True)
    foto_esboco = models.CharField(max_length=255, null=True, blank=True)

class ReligiaoELocaisSagrados(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    religiao = models.CharField(max_length=255, null=True, blank=True)
    tempo_chegar_igreja = models.CharField(max_length=255, null=True, blank=True)
    onde_enterra_entequeridos = models.CharField(max_length=100, null=True, blank=True)
    familia_tem_campas = models.CharField(max_length=10, null=True, blank=True)
    frequencia_com_que_vai_cemiterio = models.CharField(max_length=255, null=True, blank=True)

class Pecuaria(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    familia_cria_animais = models.CharField(max_length=10, null=True, blank=True)
    familia_possui_arvores = models.CharField(max_length=10, null=True, blank=True)

class ArvoreFruta(models.Model):
    pecuaria = models.ForeignKey(Pecuaria, on_delete=models.CASCADE)
    arvore_de_frutas = models.CharField(max_length=255, null=True, blank=True)
    outra_arvore_de_fruta = models.CharField(max_length=255, null=True, blank=True)
    quantidade_arvores = models.PositiveIntegerField(null=True, blank=True)
    idade_arvores = models.PositiveIntegerField(null=True, blank=True)
    tempo_producao_frutas = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class ResolucaoConflitos(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    a_quem_recorre_em_caso_de_conflitos = models.TextField(null=True, blank=True)
    outra_fonte_a_que_recorre = models.TextField(null=True, blank=True)
    metodo_para_receber_informacao = models.TextField(null=True, blank=True)
    metodo_para_dar_informacao = models.TextField(null=True, blank=True)

class ServicosPublicos(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    donde_busca_agua_para_uso_na_familia = models.CharField(max_length=255, null=True, blank=True)
    outro = models.CharField(max_length=255, null=True, blank=True)
    quantidade_bidoes = models.PositiveIntegerField(null=True, blank=True)
    tipo_tratamento_agua = models.CharField(max_length=255, null=True, blank=True)
    tempo_levado_para_chegar_local_agua = models.CharField(max_length=255, null=True, blank=True)
    como_vai_buscar_agua = models.CharField(max_length=255, null=True, blank=True)
    quem_vai_buscar_agua = models.CharField(max_length=255, null=True, blank=True)
    principal_fonte_energia_usada_para_cozinha = models.CharField(max_length=255, null=True, blank=True)
    tempo_para_chegar_local_da_fonte_energia = models.CharField(max_length=255, null=True, blank=True)
    meio_transporte_para_local_recolha_energia = models.CharField(max_length=255, null=True, blank=True)
    fonte_energia_para_iluminacao_casa = models.CharField(max_length=255, null=True, blank=True)
    outra_fonte_para_iluminacao_casa = models.CharField(max_length=255, null=True, blank=True)
    tempo_para_chegar_local_compra_fonte_energia = models.CharField(max_length=255, null=True, blank=True)

class EducacaoSaude(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    existe_escola_no_bairro = models.CharField(max_length=10, null=True, blank=True)
    tem_membro_estudante = models.CharField(max_length=10, null=True, blank=True)
    quantos_membros = models.PositiveIntegerField(null=True, blank=True)
    escola_que_frequentam_criancas_familia_count = models.PositiveIntegerField(null=True, blank=True)
    existe_centro_saude = models.CharField(max_length=10, null=True, blank=True)
    nome_centro_saude = models.CharField(max_length=100, null=True, blank=True)
    onde_procura_tratamento = models.CharField(max_length=100, null=True, blank=True)
    tempo_para_chegar_local_tratamento = models.CharField(max_length=255, null=True, blank=True)
    doencas_familia_sofre_mais = models.TextField(null=True, blank=True)  # Since there can be multiple diseases

class ExpectativasTratamento(models.Model):
    inquerito = models.OneToOneField(Inquerito, on_delete=models.CASCADE)
    ao_sair_do_lugar_o_que_espera_como_compensacao = models.TextField(null=True, blank=True)
    outra_compensacao_esperada = models.TextField(null=True, blank=True)
    onde_gostaria_de_ser_reassentado = models.TextField(null=True, blank=True)
    foto_esboco_estrutura = models.CharField(max_length=255, null=True, blank=True)
    termo_consentimento = models.CharField(max_length=255, null=True, blank=True)

