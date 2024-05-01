from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def main(request):
    hw = ['ProLiant_and_Apollo',
          'BladeSystem',
          'Synergy',
          'SimpliVity',
          'B-series_SAN',
          'Aruba_Switches',
          'Aruba_Routers',
          'FlexNetwork_Switches',
          'FlexFabric_Switches',
          'OfficeConnect_Switches',
          'Aruba_Mobility_Controllers',
          'Aruba_Hotspots',
          'MSA',
          'Nimble',
          '3PAR-Primera',
          'Autoloader_and_MSL',
          'StoreOnce',
          'StoreEasy',
          ]
    hw_disciplines = ['Part_Replacement',
                      'Rack_Mounting',
                      'Cabling',
                      'Startup',
                      'Basic_Configuration',
                      'Log_Collection',
                      'Log_Parsing',
                      'Diagnostics',
                      'Configuration_Design',
                      'Firmware_Update',
                      'Performance_Metrics_Setup',
                      'Performance_Collection'
                      ]

    sw = ['Microsoft Windows Server',
          'Red Hat Enterprise Linux',
          'SUSE Linux Enterprise Server',
          'VMware vSphere',
          'Microsoft Hyper-V',
          'Red Hat Enterprise Virtualization',
          'SUSE Xen Virtualization',
          'SUSE KVM Virtualization',
          'Docker',
          'Kubernetes',
          'Microsoft Failover Cluster',
          'Red Hat High Availability Add-On',
          'SUSE Linux Enterprise High Availability Extension',
          'Microfocus Data Protector',
          'Veeam Backup & Replication',
          'DellEMC NetWorker',
          'Veritas NetBackup',
          'Veritas Backup Exec',
          'Microsoft SQL Server',
          'Oracle Database',
          'PostgreSQL',
          'MySQL/MariaDB'
          ]
    sw_disciplines = ['Installation',
                      'Basic Configuration',
                      'Fine Tuning',
                      'Performance Collection',
                      'Performance Tuning'
                      ]

    skills = ['PRINCE2 Project Management',
              'PMI Project Management',
              'TOGAF Enterprise Architecture',
              'Technical Writing',
              'Negotiations with Customer',
              'Correspondence with Customer',
              'Performance Analysis (Statistics)',
              'Solution High Level Design',
              'Solution Low Level Design',
              'Customer Presentations',
              'Testing and Acceptance Planning',
              'Technical Training Delivery',
              'Technical Training Development',
              'ITIL/ITSM'
              ]
    skill_disciplines = ['level']

    levels = ['0 — None',
              '1 — Basic',
              '2 — Middle',
              '3 — Professional',
              '4 — Expert'
              ]

    data = {'HW': hw,
            'hw_disciplines': hw_disciplines,
            'sw': sw,
            'sw_disciplines': sw_disciplines,
            'skills': skills,
            'skill_disciplines': skill_disciplines,
            'levels': levels}
    return render(request, 'self_assessment.html', data)
