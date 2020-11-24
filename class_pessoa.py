from datetime import datetime, timedelta
import pandas as pd
import random

# DICIONÁRIO DE PALAVRAS

# TODO: FIXO obs e tipo_h, cargo, aspa, doar e org.
tipo_h = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'AB'}

obs = {0: 'EXERCE ATIVIDADE REMUNERADA;', 1: 'A;', 2: 'B;', 3: 'C;', 4: 'D;', 5: 'E;', 6: 'F;', 7: 'G;', 8: 'H;',
       9: 'I;', 10: 'J;', 11: 'K;', 12: 'L;', 13: 'M;', 14: 'N;', 15: 'O;', 16: 'P;', 17: 'Q;', 18: 'R;', 19: 'S;',
       20: 'T;', 21: 'U;', 22: 'V;', 23: 'W;', 24: 'X;', 25: 'Y;', 26: 'Z;'}

cargo = {0: 'DIRETOR', 1: 'COORDENADOR', 2: 'PRESIDENTE'}

aspa = {0: 'COM AVRB VIUVEZ', 1: 'COM AVRB DIVÓRCIO'}

org = {0: 'SDS', 1: 'SSP', 2: 'POM', 3: 'SNJ', 4: 'SPTC', 5: 'SESP', 6: 'SJS', 7: 'POF', 8: 'SES', 9: 'SEJ'}
# ------------------------------------------------------------------------------------------------------------------


class Person:
    def __init__(self):
        # RESOLVIDOS
        self.nome = []
        self.s_nome = []
        self.cpf = []
        self.rg = []
        self.folha = []
        self.pis = []
        self.n_reg = []
        self.n_5 = []
        self.n_6 = []
        self.n_9 = []
        self.n_11 = []
        self.cod_4 = []
        self.cod_8 = []
        self.cod_10 = []
        self.cod_11 = []
        self.est = []
        self.cid = []
        self.local = []
        self.d_orig = []
        self.data = []
        self.via = []
        self.n_via = []
        self.org = []
        self.rg_org_est = []

        self.tipo_h = []
        self.obs = []
        self.cargo = []
        self.aspa = []

    def set_nome(self, qtd_chars):
        file = open(r'./files/nome.txt')
        names = file.readlines()

        full_name = ''
        for i in range(3):
            random.seed()
            sel_num = random.randint(0, len(names) - 1)
            full_name = full_name+(names[sel_num].rstrip('\n'))+''

        full_name = full_name[:len(full_name)-1]

        if len(full_name) > qtd_chars:
            full_name = full_name[0:qtd_chars]
        self.nome.append(full_name)
        return full_name

    # TODO: Pode dar merda.
    def set_s_nome(self):
        file = open(r'./files/s_nome.txt')
        s_nomes = file.readlines()

        random.seed()
        sel_num = random.randint(0, len(s_nomes) - 1)
        sobrenome = (s_nomes[sel_num].rstrip('\n'))
        sobrenome = sobrenome.upper()

        self.s_nome.append(sobrenome)
        return sobrenome

    def set_cpf(self):
        def formata_cpf(n_cpf):
            formatado = ''
            for i in range(len(n_cpf)):
                formatado = formatado + n_cpf[i]

                if i == 2 or i == 5:
                    formatado = formatado + '.'
                elif i == 8:
                    formatado = formatado + '-'

            return formatado

        def dig_verificador(n_cpf):
            int_values = []

            if len(n_cpf) == 9:
                peso = 10
            else:
                peso = 11

            for i in range(len(n_cpf)):
                int_values.append(int(n_cpf[i]) * (peso - i))

            soma = sum(int_values)
            resto = soma % 11

            if resto == 0 or resto == 1:
                dig = '0'
            else:
                dig = str(11 - resto)
            return dig

        def make_cpf():
            seq_cpf = ''

            for _ in range(9):
                random.seed()
                sel_num = random.randint(0, 9)
                seq_cpf = seq_cpf + str(sel_num)

            f_dig = dig_verificador(seq_cpf)
            seq_cpf = seq_cpf + f_dig

            s_dig = dig_verificador(seq_cpf)
            seq_cpf = seq_cpf + s_dig

            seq_cpf = formata_cpf(seq_cpf)
            return seq_cpf

        r_cpf = make_cpf()
        self.cpf.append(r_cpf)
        return r_cpf

    def set_rg(self, tipo_doc):
        def formata_rg(n_rg):
            rg_f = ''
            for i in range(len(n_rg)):
                rg_f = rg_f + n_rg[i]

                if i == 1 or i == 4:
                    rg_f = rg_f + '.'
                elif i == 7:
                    rg_f = rg_f + '-'

            return rg_f

        def verf_rg(n_rg):
            dig_v = str(random.randint(0, 9))
            int_values = []
            peso = 2

            for i in range(len(n_rg)):
                int_values.append(int(n_rg[i]) * (peso + i))
            soma = sum(int_values)

            for x in range(0, 10):
                result = soma + (x * 100)
                if result % 11 == 0:
                    dig_v = str(x)
                    break
                else:
                    pass

            return dig_v

        def make_rg():
            seq_rg = ''
            for _ in range(8):
                random.seed()
                sel_num = random.randint(0, 9)
                seq_rg = seq_rg + str(sel_num)

            dig = verf_rg(seq_rg)
            seq_rg = seq_rg + dig

            # TODO: CNH comenta o formata_rg
            if tipo_doc == 'RG':
                seq_rg = formata_rg(seq_rg)

            return seq_rg

        r_rg = make_rg()
        self.rg.append(r_rg)
        return r_rg

    def set_n_9(self, qtd_chars):
        def verf_cnh_num_espelho(espelho):
            int_values = []
            peso = 10

            for x in range(len(espelho)):
                int_values.append(int(espelho[x]) * (peso - x))
            soma = sum(int_values)
            resto = soma % 11

            if resto == 0 or resto == 1:
                dig = '0'
            else:
                dig = str(11 - resto)
            return dig

        def make_n_9():
            seq_n_9 = ''
            for _ in range(8):
                random.seed()
                sel_num = random.randint(0, 9)
                seq_n_9 = seq_n_9 + str(sel_num)
            dig_v = verf_cnh_num_espelho(seq_n_9)
            seq_n_9 = seq_n_9 + dig_v
            return seq_n_9

        r_n_9 = make_n_9()

        if len(r_n_9) > qtd_chars:
            r_n_9 = r_n_9[0:qtd_chars]

        self.n_9.append(r_n_9)
        return r_n_9

    def set_folha(self):
        c_nasc = 'C.NAS='
        a_folha = 'FL='
        livro = 'LV='

        lista = random.sample(range(1, 500), 3)
        c_nasc = c_nasc+str(lista[0])+' '
        livro = livro + str(lista[1])+' '
        a_folha = a_folha+str(lista[2])

        final = c_nasc+livro+a_folha
        self.folha.append(final)
        return final

    def set_pis(self, qtd_chars):
        pis_pasep = ''
        for x in range(9):
            random.seed()
            sel_num = random.randint(0, 9)
            pis_pasep = pis_pasep + str(sel_num)
            if x == 4:
                pis_pasep = pis_pasep+'/'
            else:
                pass

        if len(pis_pasep) > qtd_chars:
            pis_pasep = pis_pasep[0:qtd_chars]
        self.pis.append(pis_pasep)
        return pis_pasep

    def set_n_5(self):
        seq_n_5 = ''
        for x in range(5):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_n_5 = seq_n_5 + str(sel_num)
            if x == 3:
                seq_n_5 = seq_n_5 + '-'
            else:
                pass

        self.n_5.append(seq_n_5)
        return seq_n_5

    def set_n_6(self):
        seq_n_6 = ''
        for x in range(5):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_n_6 = seq_n_6 + str(sel_num)

        self.n_6.append(seq_n_6)
        return seq_n_6

    def set_cod_4(self):
        seq_n_nh = 'NH '
        for x in range(2):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_n_nh = seq_n_nh + str(sel_num)

        self.cod_4.append(seq_n_nh)
        return seq_n_nh

    def set_cod_8(self):
        seq_cod_8 = ''
        for x in range(7):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_cod_8 = seq_cod_8 + str(sel_num)

        self.cod_8.append(seq_cod_8)
        return seq_cod_8

    def set_cod_10(self):
        alfabeto = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        random.seed()
        sel_letra = random.randint(0, len(alfabeto)-1)

        seq_cod_10 = alfabeto[sel_letra]

        for x in range(8):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_cod_10 = seq_cod_10 + str(sel_num)
            if x == 2:
                seq_cod_10 = seq_cod_10 + '-'
            else:
                pass

        self.cod_10.append(seq_cod_10)
        return seq_cod_10

    def set_est(self):
        random.seed()
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        sel_num = random.randint(0, df.shape[0] - 1)

        sel_est = df['UF'][sel_num].upper()
        self.est.append(sel_est)
        return sel_est

    def set_cid(self, qtd_chars):
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        df_filter = (df.loc[df['Município'].apply(lambda x: len(x) < qtd_chars)]).dropna(how='all')

        if df_filter.shape[0] > 0:
            random.seed()
            sel_num = random.randint(0, df_filter.shape[0] - 1)
            sel_cid = df_filter['Município'].values[sel_num].upper()
        else:
            sel_cid = 'ITU'

        self.cid.append(sel_cid)
        return sel_cid

    def set_cid_est(self, qtd_chars):
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        df_filter = (df.loc[df['Município'].apply(lambda x: len(x) < qtd_chars-4)]).dropna(how='all')

        if df_filter.shape[0] > 0:
            random.seed()
            sel_num = random.randint(0, df_filter.shape[0]-1)
            sel_est = df_filter['UF'].values[sel_num].upper()
            sel_cid = df_filter['Município'].values[sel_num].upper()
            sel_local = sel_cid + '-' + sel_est
        else:
            sel_local = 'ITU-SP'

        self.local.append(sel_local)
        return sel_local

    # TODO: Checar get_cid
    def set_d_orig(self):
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        random.seed()
        sel_num = random.randint(0, len(df) - 1)
        sel_cid = df['Município'][sel_num].upper()
        sel_est = df['UF'].values[sel_num].upper()

        doc = 'CMC= ' + sel_cid + '-' + sel_est + ' ,SEDE'
        self.d_orig.append(doc)
        return doc

    def set_n_reg(self):
        seq_n_reg = ''
        for x in range(11):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_n_reg = seq_n_reg + str(sel_num)

        self.n_reg.append(seq_n_reg)
        return seq_n_reg

    def set_n_11(self):
        seq_n_11 = ''
        for x in range(11):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_n_11 = seq_n_11 + str(sel_num)

        self.n_11.append(seq_n_11)
        return seq_n_11

    def set_cod_11(self):
        random.seed()
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        sel_num = random.randint(0, df.shape[0] - 1)
        seq_cod_11 = df['UF'][sel_num].upper()
        for x in range(9):
            random.seed()
            sel_num = random.randint(0, 9)
            seq_cod_11 = seq_cod_11 + str(sel_num)

        self.cod_11.append(seq_cod_11)
        return seq_cod_11

    def set_data(self):
        def gen_datetime(min_year=1950, max_year=datetime.now().year):
            start = datetime(min_year, 1, 1, 00, 00, 00)
            years = max_year - min_year + 1
            end = start + timedelta(days=365 * years)
            date_f = start + (end - start) * random.random()
            return str(date_f)

        full_data = gen_datetime().split(' ')
        full_data = full_data[0].split('-')
        date = full_data[2] + '/' + full_data[1] + '/' + full_data[0]

        self.data.append(date)
        return date

    def set_org(self):
        random.seed()
        sel_num = random.randint(0, len(org)-1)
        text = org[sel_num]
        self.org.append(text)
        return text

    def set_rg_org_est(self):
        random.seed()
        sel_num = random.randint(0, len(org)-1)
        org_p = org[sel_num]

        random.seed()
        df = pd.read_csv(r'./files/cid_est.csv', encoding='utf-8')
        sel_num_est = random.randint(0, len(df) - 1)
        est_p = df['UF'][sel_num_est].upper()

        rg_p = self.set_rg(tipo_doc='CNH')

        final = rg_p + ' ' + org_p + ' ' + est_p

        self.rg_org_est.append(final)
        return final

    def set_via(self):
        random.seed()
        sel_num = random.randint(1, 9)
        via_p = str(sel_num) + ' VIA'
        self.via.append(via_p)
        return via_p

    def set_n_via(self):
        random.seed()
        sel_num = random.randint(1, 9)
        num_via = '0' + str(sel_num)
        self.n_via.append(num_via)
        return num_via

    def set_obs(self):
        text = ''
        random.seed()
        sel_num = random.randint(0, len(obs)-1)
        text = obs[sel_num]
        self.obs.append(text)
        return text

    def set_cargo(self):
        random.seed()
        sel_num = random.randint(0, len(cargo)-1)
        text = cargo[sel_num]
        self.cargo.append(text)
        return text

    def set_tipo_h(self):
        random.seed()
        sel_num = random.randint(0, len(tipo_h)-1)
        text = tipo_h[sel_num]
        self.tipo_h.append(text)
        return text

    def set_aspa(self):
        random.seed()
        sel_num = random.randint(0, 1)
        text = aspa[sel_num]
        self.aspa.append(text)
        return text

    def get_nome(self):
        topo = self.nome.pop(0)
        self.nome.append(topo)
        return topo

    def get_s_nome(self):
        topo = self.s_nome.pop(0)
        self.s_nome.append(topo)
        return topo

    def get_cpf(self):
        topo = self.cpf.pop(0)
        self.cpf.append(topo)
        return topo

    def get_rg(self):
        topo = self.rg.pop(0)
        self.rg.append(topo)
        return topo

    def get_org(self):
        topo = self.org.pop(0)
        self.org.append(topo)
        return topo

    def get_est(self):
        topo = self.est.pop(0)
        self.est.append(topo)
        return topo

    def get_cid(self):
        topo = self.cid.pop(0)
        self.cid.append(topo)
        return topo

    def get_rg_org_est(self):
        topo = self.rg_org_est.pop(0)
        self.rg_org_est.append(topo)
        return topo

    def get_data(self):
        topo = self.data.pop(0)
        self.data.append(topo)
        return topo

    def get_tipo_h(self):
        topo = self.tipo_h.pop(0)
        self.tipo_h.append(topo)
        return topo

    def get_n_reg(self):
        topo = self.n_reg.pop(0)
        self.n_reg.append(topo)
        return topo

    def get_n_9(self):
        topo = self.n_9.pop(0)
        self.n_9.append(topo)
        return topo

    def get_n_11(self):
        topo = self.n_11.pop(0)
        self.n_11.append(topo)
        return topo

    def get_cod_11(self):
        topo = self.cod_11.pop(0)
        self.cod_11.append(topo)
        return topo

    def get_local(self):
        topo = self.local.pop(0)
        self.local.append(topo)
        return topo

    def get_obs(self):
        topo = self.obs.pop(0)
        self.obs.append(topo)
        return topo

    def get_cargo(self):
        topo = self.cargo.pop(0)
        self.cargo.append(topo)
        return topo

    def get_via(self):
        topo = self.via.pop(0)
        self.via.append(topo)
        return topo

    def get_folha(self):
        topo = self.folha.pop(0)
        self.folha.append(topo)
        return topo

    def get_d_orig(self):
        topo = self.d_orig.pop(0)
        self.d_orig.append(topo)
        return topo

    def get_aspa(self):
        topo = self.aspa.pop(0)
        self.aspa.append(topo)
        return topo

    def get_cod_4(self):
        topo = self.cod_4.pop(0)
        self.cod_4.append(topo)
        return topo

    def get_pis(self):
        topo = self.pis.pop(0)
        self.pis.append(topo)
        return topo

    def get_n_5(self):
        topo = self.n_5.pop(0)
        self.n_5.append(topo)
        return topo

    def get_cod_10(self):
        topo = self.cod_10.pop(0)
        self.cod_10.append(topo)
        return topo

    def get_cod_8(self):
        topo = self.cod_8.pop(0)
        self.cod_8.append(topo)
        return topo

    def get_n_via(self):
        topo = self.n_via.pop(0)
        self.n_via.append(topo)
        return topo

    def get_n_6(self):
        topo = self.n_6.pop(0)
        self.n_6.append(topo)
        return topo

