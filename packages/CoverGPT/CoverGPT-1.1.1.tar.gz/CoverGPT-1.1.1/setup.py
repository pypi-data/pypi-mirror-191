from distutils.core import setup
setup(
  name = 'CoverGPT',    
  packages = ['CoverGPT'], 
  version = '1.1.1',
  license='gpl-3.0',
  description = 'Generate a personalized and formatted cover letter for a given job position, using your resume to add personalized details. Utilizes ChatGPT.',   # Give a short description about your library
  author = 'Mohammad Mahfooz',  
  author_email = 'mohammadmahfoozpersonal@gmail.com', 
  url = 'https://github.com/mahfoozm/CoverGPT',
  download_url = 'https://github.com/mahfoozm/CoverGPT/archive/refs/tags/v1.1.1.tar.gz',
  keywords = ['ChatGPT', 'AI', 'Cover Letter'],
  install_requires=[
          'customtkinter==5.0.3',
          'PyPDF2==3.0.1',
          'revChatGPT==2.2.0'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
  ],
  package_data={'CoverGPT': ['template.tex', 'cover.cls', 'OpenFonts/*', 'OpenFonts/fonts/lato/*', 'OpenFonts/fonts/raleway/*']},
)