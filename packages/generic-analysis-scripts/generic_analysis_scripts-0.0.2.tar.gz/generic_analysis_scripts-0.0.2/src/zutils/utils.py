import zfit
import numpy

import pandas            as pnd
import matplotlib.pyplot as plt

import utils_noroot      as utnr

#-------------------------------------------------------
class data:
    log = utnr.getLogger(__name__)
#-------------------------------------------------------
def copy_model(pdf):
    '''
    Ment to copy PDF's to bypass dropped normlization
    when copying extended PDFs
    '''
    if not pdf.is_extended:
        return pdf.copy()

    yld = pdf.get_yield()

    pdf = pdf.copy()

    pdf = pdf.create_extended(yld)

    return pdf
#-------------------------------------------------------
def result_to_latex(res, tex_path):
    '''
    Takes result object and dumps table with values of
    parameters to latex table
    '''

    #Can't freeze twice, freeze just in case
    try:
        res.freeze()
    except AttributeError:
        pass

    d_tab              = {}
    d_tab['Parameter'] = [ nam                     for nam,  _ in res.params.items()]
    d_tab['Value'    ] = [ dc['value']             for   _, dc in res.params.items()]
    try:
        d_tab['Error'    ] = [ dc['hesse']['error'] for   _, dc in res.params.items()]
    except:
        data.log.warning(f'Not including errors, run: res.hesse(name=\'hesse_np\')')

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def pdf_to_latex(pdf, tex_path):
    '''
    Takes pdf and dumps table with values of
    parameters to latex table
    '''

    l_par = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False)) 

    d_tab              = {}
    d_tab['Parameter'] = [ par.name     for par in l_par]
    d_tab['Value'    ] = [ par.numpy()  for par in l_par]
    d_tab['Floating' ] = [ par.floating for par in l_par]

    df = pnd.DataFrame(d_tab)
    df.to_latex(tex_path, index=False)
#-------------------------------------------------------
def get_pdf_params(pdf, floating=True):
    '''
    Takes PDF 
    Returns {parname -> value} dictionary
    '''

    l_par = pdf.get_params(floating=floating)

    d_par = { par.name : par.value().numpy() for par in l_par }

    return d_par
#-------------------------------------------------------
def fix_pars(pdf, d_par):
    '''
    Will take a pdf and a {var_name -> [val, err]} map. It will fix the values of the parameters
    of the PDF according to the dictionary.

    Returns PDF with fixed parameters
    '''

    l_par     = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))
    d_par_pdf = { par.name : par for par in l_par }

    data.log.info('Fixing PDF parameters')
    for par_name, [val, _] in d_par.items():
        par = d_par_pdf[par_name]
        par.set_value(val)
        par.floating = False

        data.log.info(f'{par_name:<30}{"->":20}{val:<20}')

    return pdf
#-------------------------------------------------------

