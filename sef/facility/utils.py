"""Case Utils"""
from xhtml2pdf.pisa import CreatePDF
from django.template import loader, Context


def extract_resorce(p_resource, resource_index, ns):
    if not isinstance(p_resource.find(resource_index, ns), type(None)):
        return p_resource.find(resource_index, ns).text
    else:
        return None


def get_platform(platform):
    if platform == 'IOS':
        platform = 'iphone'

    if platform == 'ANDROID':
        platform = 'android'

    return platform

def get_extracts(extracts):
    decoded_extracts = []
    for ext in extracts:
        if ext == 'Calls':
            extract = 'call'
            decoded_extracts.append(extract)

        if ext == 'Messages':
            extract = 'message'
            decoded_extracts.append(extract)

        if ext == 'Location':
            extract = 'location'
            decoded_extracts.append(extract)

    return decoded_extracts


def generate_nugget_dsl(platform, file_path, extract):
    dsl = f'{platform}{extract}'
    fname = 'nugget_dsl_{}_{}.txt'.format(platform, extract)
    dsl_fpath = '/tmp/' + fname

    f = open(dsl_fpath, 'w+')
    f.write(f'construct_{dsl}="{platform}:{file_path}" | extract as {extract}\n')
    f.write(f'print construct_{dsl} as dfxml')
    f.close()

    return dsl_fpath
