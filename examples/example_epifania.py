"""
Example: Complete Mass for the Solemnity of the Epiphany
Similar to: https://arquisp.org.br/wp-content/uploads/2025/10/Ano-50A-09-SOLENIDADE-DA-EPIFANIA-DO-SENHOR.pdf
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.custom_mass import CustomMass


def create_epiphany_mass():
    """Create a complete Mass for the Solemnity of the Epiphany"""
    
    mass = CustomMass()
    
    # Set celebration details
    mass.set_celebration(
        name="Solenidade da Epifania do Senhor",
        date_str="2026-01-06",
        celebration_type="solenidade",
        color="branco",
        season="Tempo do Natal"
    )
    
    # RITOS INICIAIS
    mass.set_entrance_antiphon(
        text="Eis que vem o Senhor soberano; o reino e o poder e o império estão em suas mãos.",
        reference="Cf. Ml 3,1; 1Cr 29,12"
    )
    
    mass.set_part_content("greeting", 
        "Sacerdote: Em nome do Pai, do Filho e do Espírito Santo.\n"
        "Povo: Amém.\n\n"
        "Sacerdote: A graça de nosso Senhor Jesus Cristo, o amor do Pai e a comunhão do Espírito Santo estejam convosco.\n"
        "Povo: Bendito seja Deus que nos reuniu no amor de Cristo."
    )
    
    mass.set_part_content("penitential",
        "Sacerdote: Irmãos e irmãs, reconheçamos as nossas culpas para celebrarmos dignamente os santos mistérios.\n\n"
        "(Pausa para reflexão)\n\n"
        "Todos: Confesso a Deus todo-poderoso e a vós, irmãos e irmãs, que pequei muitas vezes por pensamentos e palavras, "
        "atos e omissões, por minha culpa, minha tão grande culpa. E peço à Virgem Maria, aos anjos e santos e a vós, "
        "irmãos e irmãs, que rogueis por mim a Deus, nosso Senhor."
    )
    
    mass.set_part_content("kyrie",
        "Senhor, tende piedade de nós.\n"
        "R. Senhor, tende piedade de nós.\n\n"
        "Cristo, tende piedade de nós.\n"
        "R. Cristo, tende piedade de nós.\n\n"
        "Senhor, tende piedade de nós.\n"
        "R. Senhor, tende piedade de nós."
    )
    
    mass.set_part_content("gloria",
        "Glória a Deus nas alturas,\n"
        "e paz na terra aos homens por ele amados.\n"
        "Senhor Deus, rei dos céus,\n"
        "Deus Pai todo-poderoso:\n"
        "nós vos louvamos,\n"
        "nós vos bendizemos,\n"
        "nós vos adoramos,\n"
        "nós vos glorificamos,\n"
        "nós vos damos graças, por vossa imensa glória.\n\n"
        "Senhor Jesus Cristo, Filho Unigênito,\n"
        "Senhor Deus, Cordeiro de Deus, Filho de Deus Pai.\n"
        "Vós que tirais o pecado do mundo, tende piedade de nós.\n"
        "Vós que tirais o pecado do mundo, acolhei a nossa súplica.\n"
        "Vós que estais à direita do Pai, tende piedade de nós.\n\n"
        "Só vós sois o Santo, só vós, o Senhor,\n"
        "só vós, o Altíssimo, Jesus Cristo,\n"
        "com o Espírito Santo, na glória de Deus Pai.\n"
        "Amém."
    )
    
    mass.set_part_content("collect",
        "Oremos.\n\n"
        "Ó Deus, que neste dia revelastes vosso Filho às nações, guiando-as pela estrela, "
        "concedei aos vossos filhos e filhas, que já vos conhecemos pela fé, "
        "chegar à contemplação da vossa glória.\n"
        "Por nosso Senhor Jesus Cristo, vosso Filho, na unidade do Espírito Santo.\n\n"
        "R. Amém."
    )
    
    # LITURGIA DA PALAVRA
    mass.set_part_content("first_reading",
        "Leitura do Livro do Profeta Isaías (60,1-6)\n\n"
        "Levanta-te, acende as lâmpadas, Jerusalém, porque chegou tua luz "
        "e a glória do Senhor nasceu sobre ti! Eis que as trevas cobrem a terra "
        "e a escuridão, os povos; mas sobre ti levanta o Senhor e sua glória em ti aparece.\n\n"
        "Os povos caminham à tua luz, e os reis, ao clarão de tua aurora. "
        "Levanta os olhos ao redor e observa: todos estes se ajuntaram e vieram a ti; "
        "teus filhos vêm de longe, e tuas filhas são trazidas no colo.\n\n"
        "Então verás, ficarás radiante, teu coração estremecerá e se dilatará. "
        "Porque virão a ti os tesouros do mar, as riquezas das nações a ti afluirão; "
        "multidões de camelos te cobrirão, dromedários de Madiã e de Efá; "
        "todos virão de Sabá, trazendo ouro e incenso e proclamando os louvores do Senhor.\n\n"
        "Palavra do Senhor.\n"
        "R. Graças a Deus."
    )
    
    mass.set_part_content("psalm",
        "Salmo 71(72)\n\n"
        "R. Todos os reis hão de adorá-lo, e as nações vão servi-lo.\n\n"
        "Ó Deus, dai ao rei vosso julgamento\n"
        "e vossa justiça ao filho do rei;\n"
        "que ele julgue com justiça vosso povo\n"
        "e os vossos pobres com retidão. R.\n\n"
        "Em seus dias floresça a justiça\n"
        "e reine a paz para sempre!\n"
        "Seu domínio de mar a mar se estenda,\n"
        "do Grande Rio até aos confins da terra. R.\n\n"
        "Os reis de Társis e das ilhas hão de vir\n"
        "e oferecer seus dons em homenagem.\n"
        "Todos os reis hão de adorá-lo,\n"
        "e as nações vão servi-lo. R.\n\n"
        "Porque libertará o pobre que suplica\n"
        "e o infeliz que não tem amparo.\n"
        "Apieda-se do fraco e do indigente,\n"
        "e a vida dos pobres ele salva. R."
    )
    
    mass.set_part_content("second_reading",
        "Leitura da Carta de São Paulo Apóstolo aos Efésios (3,2-3a.5-6)\n\n"
        "Irmãos: Certamente ouvistes falar da missão da graça de Deus que me foi confiada em vosso favor. "
        "Por uma revelação, fez-me conhecer este mistério.\n\n"
        "Este mistério não foi dado a conhecer aos homens das gerações passadas, "
        "mas agora foi revelado pelo Espírito aos seus santos apóstolos e profetas: "
        "os pagãos são admitidos à mesma herança, são membros do mesmo corpo, "
        "são associados à mesma promessa em Jesus Cristo, por meio do Evangelho.\n\n"
        "Palavra do Senhor.\n"
        "R. Graças a Deus."
    )
    
    mass.set_part_content("gospel_acclamation",
        "R. Aleluia, Aleluia, Aleluia.\n\n"
        "Vimos a sua estrela no oriente\n"
        "e viemos adorar o Senhor.\n\n"
        "R. Aleluia, Aleluia, Aleluia."
    )
    
    mass.set_part_content("gospel",
        "O Senhor esteja convosco.\n"
        "R. Ele está no meio de nós.\n\n"
        "Proclamação do Evangelho de Jesus Cristo segundo São Mateus (2,1-12)\n\n"
        "R. Glória a vós, Senhor!\n\n"
        "Tendo nascido Jesus na cidade de Belém, na Judeia, no tempo do rei Herodes, "
        "eis que alguns magos do Oriente chegaram a Jerusalém, perguntando: "
        "'Onde está o rei dos judeus que acaba de nascer? Nós vimos a sua estrela no Oriente "
        "e viemos adorá-lo.'\n\n"
        "Ao saber disso, o rei Herodes ficou perturbado, assim como toda a cidade de Jerusalém. "
        "Reunindo todos os sumos sacerdotes e os mestres da Lei, perguntava-lhes onde o Messias deveria nascer. "
        "Eles responderam: 'Em Belém, na Judeia, pois assim foi escrito pelo profeta: "
        "\"E tu, Belém, terra de Judá, de modo algum és a menor entre as principais cidades de Judá, "
        "porque de ti sairá um chefe que vai ser o pastor de Israel, o meu povo.\"'\n\n"
        "Então Herodes chamou em segredo os magos e procurou saber deles cuidadosamente "
        "quando a estrela tinha aparecido. Depois os enviou a Belém, dizendo: "
        "'Ide e procurai obter informações exatas sobre o menino. E, quando o encontrardes, "
        "avisai-me, para que também eu vá adorá-lo.'\n\n"
        "Depois que ouviram o rei, eles partiram. E a estrela, que tinham visto no Oriente, "
        "ia adiante deles, até parar sobre o lugar onde estava o menino. "
        "Ao verem de novo a estrela, os magos sentiram uma alegria muito grande. "
        "Quando entraram na casa, viram o menino com Maria, sua mãe. "
        "Ajoelharam-se diante dele e o adoraram. Depois abriram seus cofres e lhe ofereceram presentes: "
        "ouro, incenso e mirra.\n\n"
        "Avisados em sonho para não voltarem a Herodes, retornaram para a sua terra, seguindo outro caminho.\n\n"
        "Palavra da Salvação.\n"
        "R. Glória a vós, Senhor!"
    )
    
    mass.set_part_content("homily",
        "(Espaço para a homilia do celebrante)"
    )
    
    mass.set_part_content("creed",
        "Creio em um só Deus, Pai todo-poderoso,\n"
        "criador do céu e da terra,\n"
        "de todas as coisas visíveis e invisíveis.\n\n"
        "Creio em um só Senhor, Jesus Cristo,\n"
        "Filho Unigênito de Deus,\n"
        "nascido do Pai antes de todos os séculos:\n"
        "Deus de Deus, Luz da Luz,\n"
        "Deus verdadeiro de Deus verdadeiro;\n"
        "gerado, não criado, consubstancial ao Pai.\n"
        "Por ele todas as coisas foram feitas.\n\n"
        "E por nós, homens, e para nossa salvação,\n"
        "desceu dos céus:\n"
        "e se encarnou pelo Espírito Santo,\n"
        "no seio da Virgem Maria, e se fez homem.\n\n"
        "Também por nós foi crucificado\n"
        "sob Pôncio Pilatos;\n"
        "padeceu e foi sepultado.\n"
        "Ressuscitou ao terceiro dia,\n"
        "conforme as Escrituras,\n"
        "e subiu aos céus, onde está sentado\n"
        "à direita do Pai.\n"
        "E de novo há de vir, em sua glória,\n"
        "para julgar os vivos e os mortos;\n"
        "e o seu reino não terá fim.\n\n"
        "Creio no Espírito Santo,\n"
        "Senhor que dá a vida,\n"
        "e procede do Pai e do Filho;\n"
        "e com o Pai e o Filho é adorado e glorificado:\n"
        "ele que falou pelos profetas.\n\n"
        "Creio na Igreja, una, santa, católica e apostólica.\n"
        "Professo um só batismo\n"
        "para remissão dos pecados.\n"
        "E espero a ressurreição dos mortos\n"
        "e a vida do mundo que há de vir.\n"
        "Amém."
    )
    
    mass.set_part_content("prayers_faithful",
        "Sacerdote: Adoremos a Cristo, o Rei dos reis, que se manifestou aos povos, e roguemos:\n"
        "R. Mostrai-nos, Senhor, vossa face!\n\n"
        "1. Por toda a Igreja de Deus, para que seja sinal e instrumento da salvação para todos os povos. "
        "Roguemos ao Senhor. R.\n\n"
        "2. Pela unidade dos cristãos, para que todos sejam um em Cristo. "
        "Roguemos ao Senhor. R.\n\n"
        "3. Pelos governantes das nações, para que promovam a justiça e a paz entre os povos. "
        "Roguemos ao Senhor. R.\n\n"
        "4. Pelos que buscam a verdade, para que encontrem a luz de Cristo. "
        "Roguemos ao Senhor. R.\n\n"
        "5. Por nossa comunidade, para que sejamos testemunhas da luz de Cristo no mundo. "
        "Roguemos ao Senhor. R.\n\n"
        "Sacerdote: Ó Deus, que manifestastes vosso Filho a todos os povos, "
        "acolhei as preces de vossa Igreja e conduzi todos ao conhecimento da verdade. "
        "Por Cristo, nosso Senhor.\n"
        "R. Amém."
    )
    
    # LITURGIA EUCARÍSTICA
    mass.set_part_content("offertory",
        "Canto de apresentação das oferendas\n\n"
        "(Preparação do altar e apresentação do pão e do vinho)"
    )
    
    mass.set_part_content("prayer_offerings",
        "Sacerdote: Olhai, ó Deus, as oferendas de vossa Igreja, "
        "que já não vos apresenta ouro, incenso e mirra, "
        "mas aquele que por estes dons foi anunciado, imolado e recebido, "
        "Jesus Cristo, nosso Senhor.\n\n"
        "R. Amém."
    )
    
    mass.set_part_content("preface",
        "Sacerdote: O Senhor esteja convosco.\n"
        "R. Ele está no meio de nós.\n\n"
        "Sacerdote: Corações ao alto.\n"
        "R. O nosso coração está em Deus.\n\n"
        "Sacerdote: Demos graças ao Senhor, nosso Deus.\n"
        "R. É nosso dever e nossa salvação.\n\n"
        "Na verdade, é justo e necessário, é nosso dever e salvação\n"
        "dar-vos graças, sempre e em todo o lugar,\n"
        "Senhor, Pai santo, Deus eterno e todo-poderoso.\n\n"
        "Hoje manifestastes em Cristo, luz do mundo,\n"
        "o mistério da salvação dos povos.\n"
        "E quando ele apareceu em nossa carne mortal,\n"
        "nos renovastes com a luz gloriosa da imortalidade.\n\n"
        "Por isso, com os anjos e todos os santos,\n"
        "proclamamos vossa glória, cantando a uma só voz:"
    )
    
    mass.set_part_content("sanctus",
        "Santo, Santo, Santo, Senhor Deus do universo!\n"
        "O céu e a terra proclamam a vossa glória.\n"
        "Hosana nas alturas!\n"
        "Bendito o que vem em nome do Senhor!\n"
        "Hosana nas alturas!"
    )
    
    mass.set_part_content("eucharistic_prayer",
        "(Oração Eucarística - conforme escolha do celebrante)"
    )
    
    mass.set_part_content("our_father",
        "Sacerdote: Obedientes à palavra do Salvador e formados por seu divino ensinamento, "
        "ousamos dizer:\n\n"
        "Todos: Pai nosso que estais nos céus,\n"
        "santificado seja o vosso nome;\n"
        "venha a nós o vosso reino;\n"
        "seja feita a vossa vontade,\n"
        "assim na terra como no céu.\n"
        "O pão nosso de cada dia nos dai hoje;\n"
        "perdoai-nos as nossas ofensas,\n"
        "assim como nós perdoamos a quem nos tem ofendido;\n"
        "e não nos deixeis cair em tentação,\n"
        "mas livrai-nos do mal.\n\n"
        "Sacerdote: Livrai-nos de todos os males, ó Pai,\n"
        "e dai-nos hoje a vossa paz.\n"
        "Ajudados por vossa misericórdia,\n"
        "sejamos sempre livres do pecado\n"
        "e protegidos de todos os perigos,\n"
        "enquanto, vivendo a esperança,\n"
        "aguardamos a vinda do Cristo Salvador.\n\n"
        "Povo: Vosso é o reino, o poder e a glória para sempre!"
    )
    
    mass.set_part_content("peace",
        "Sacerdote: Senhor Jesus Cristo, dissestes aos vossos Apóstolos:\n"
        "Eu vos deixo a paz, eu vos dou a minha paz.\n"
        "Não olheis os nossos pecados, mas a fé que anima vossa Igreja;\n"
        "dai-lhe, segundo o vosso desejo, a paz e a unidade.\n\n"
        "A paz do Senhor esteja sempre convosco.\n"
        "R. O amor de Cristo nos uniu.\n\n"
        "Sacerdote: Saudai-vos em Cristo, com um gesto de paz e fraternidade."
    )
    
    mass.set_part_content("agnus_dei",
        "Cordeiro de Deus, que tirais o pecado do mundo,\n"
        "tende piedade de nós.\n\n"
        "Cordeiro de Deus, que tirais o pecado do mundo,\n"
        "tende piedade de nós.\n\n"
        "Cordeiro de Deus, que tirais o pecado do mundo,\n"
        "dai-nos a paz."
    )
    
    mass.set_part_content("communion",
        "Sacerdote: Eis o Cordeiro de Deus, aquele que tira o pecado do mundo.\n"
        "Felizes os convidados para a ceia do Senhor.\n\n"
        "Todos: Senhor, eu não sou digno(a) de que entreis em minha morada,\n"
        "mas dizei uma palavra e serei salvo(a).\n\n"
        "(Momento da Comunhão)"
    )
    
    mass.set_part_content("communion_antiphon",
        "Antífona da Comunhão\n\n"
        "Nós vimos a sua estrela no Oriente\n"
        "e viemos com presentes adorar o Senhor.\n"
        "(Cf. Mt 2,2)"
    )
    
    mass.set_part_content("prayer_communion",
        "Oremos.\n\n"
        "Conduzi-nos, ó Deus, à luz eterna,\n"
        "nós que conhecemos pelo mistério admirável deste sacramento\n"
        "aquele que é luz nascida da luz.\n"
        "Por Cristo, nosso Senhor.\n\n"
        "R. Amém."
    )
    
    # RITOS FINAIS
    mass.set_part_content("announcements",
        "(Avisos da comunidade, se houver)"
    )
    
    mass.set_part_content("blessing",
        "Sacerdote: O Senhor esteja convosco.\n"
        "R. Ele está no meio de nós.\n\n"
        "Sacerdote: A bênção de Deus todo-poderoso,\n"
        "Pai, Filho e Espírito Santo,\n"
        "desça sobre vós e permaneça para sempre.\n\n"
        "R. Amém."
    )
    
    mass.set_part_content("dismissal",
        "Sacerdote: Ide em paz, e o Senhor vos acompanhe.\n"
        "R. Graças a Deus!"
    )
    
    return mass


if __name__ == "__main__":
    # Create the Epiphany Mass
    epiphany = create_epiphany_mass()
    
    # Display the complete Mass
    print(epiphany.get_full_text())
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), "epifania_2026.txt")
    epiphany.export_to_text(output_file)
    print(f"\n\nMissa completa salva em: {output_file}")
    
    # Optional: Export to PDF (requires reportlab)
    try:
        pdf_file = os.path.join(os.path.dirname(__file__), "epifania_2026.pdf")
        epiphany.export_to_pdf(pdf_file)
        print(f"PDF gerado: {pdf_file}")
    except ImportError:
        print("\nPara gerar PDF, instale: pip install reportlab")
