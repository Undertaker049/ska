from django.shortcuts import render


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

    sw = ['Microsoft_Windows_Server',
          'Red_Hat_Enterprise_Linux',
          'SUSE_Linux_Enterprise_Server',
          'VMware_vSphere',
          'Microsoft_Hyper-V',
          'Red_Hat_Enterprise_Virtualization',
          'SUSE_Xen_Virtualization',
          'SUSE_KVM_Virtualization',
          'Docker',
          'Kubernetes',
          'Microsoft_Failover_Cluster',
          'Red_Hat_High_Availability_Add-On',
          'SUSE_Linux_Enterprise_High_Availability_Extension',
          'Microfocus_Data_Protector',
          'Veeam_Backup_and_Replication',
          'DellEMC_NetWorker',
          'Veritas_NetBackup',
          'Veritas_Backup_Exec',
          'Microsoft_SQL_Server',
          'Oracle_Database',
          'PostgreSQL',
          'MySQL-MariaDB']

    sw_disciplines = ['Installation',
                      'Basic_Configuration',
                      'Fine_Tuning',
                      'Performance_Collection',
                      'Performance_Tuning']

    skills = ['PRINCE2_Project_Management',
              'PMI_Project_Management',
              'TOGAF_Enterprise_Architecture',
              'Technical_Writing',
              'Negotiations_with_Customer',
              'Correspondence_with_Customer',
              'Performance_Analysis-Statistics',
              'Solution_High_Level_Design',
              'Solution_Low_Level_Design',
              'Customer_Presentations',
              'Testing_and_Acceptance_Planning',
              'Technical_Training_Delivery',
              'Technical_Training_Development',
              'ITIL-ITSM']

    skill_disciplines = ['level']

    levels = ['— Select your level —',
              '0 — None',
              '1 — Basic',
              '2 — Middle',
              '3 — Professional',
              '4 — Expert'
              ]

    data = {'HW': hw,
            'hw_disciplines': hw_disciplines,
            'SW': sw,
            'sw_disciplines': sw_disciplines,
            'skills': skills,
            'skill_disciplines': skill_disciplines,
            'levels': levels}
    return render(request, 'self_assessment.html', data)


def test(request):
    return render(request, 'testPage.html')
