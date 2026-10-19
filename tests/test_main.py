import unittest
from app.logic import processar_solicitacao

class TestProcessamento(unittest.TestCase):
    def test_calcula_total_e_aprova_abaixo_limite(self):
        r = processar_solicitacao({"solicitacao_id":"SC-1","solicitante":"Ana","itens":[{"descricao":"Mouse","quantidade":2,"valor_unitario":"50.25"}]})
        self.assertEqual(r["total"], 100.5)
        self.assertEqual(r["decisao"], "aprovacao_automatica")
    def test_encaminha_acima_limite_para_revisao(self):
        r = processar_solicitacao({"solicitacao_id":"SC-2","solicitante":"Bia","itens":[{"descricao":"Equipamento","quantidade":1,"valor_unitario":"5000.01"}]})
        self.assertEqual(r["decisao"], "revisao_manual")
    def test_rejeita_quantidade_zero(self):
        with self.assertRaises(ValueError):
            processar_solicitacao({"solicitacao_id":"SC-3","solicitante":"Caio","itens":[{"descricao":"Item","quantidade":0,"valor_unitario":5}]})

if __name__ == "__main__":
    unittest.main()
