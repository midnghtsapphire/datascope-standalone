import { X, ExternalLink, Calendar, Shield, AlertTriangle, Building, Bug } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { getDaysUntilDue, getUrgencyColor, getSeverityBadgeVariant } from '../api.js'

const ThreatDetailsModal = ({ threat, isOpen, onClose }) => {
  if (!isOpen || !threat) return null

  const daysUntilDue = getDaysUntilDue(threat.dueDate)
  const urgencyColor = getUrgencyColor(daysUntilDue)

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  const openCVELink = () => {
    window.open(`https://nvd.nist.gov/vuln/detail/${threat.cveID}`, '_blank')
  }

  const openVendorLink = () => {
    // This would typically link to vendor-specific security advisories
    window.open(`https://www.google.com/search?q=${threat.vendorProject}+${threat.cveID}+security+advisory`, '_blank')
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={handleOverlayClick}
    >
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-3">
            <Shield className="h-6 w-6 text-blue-600" />
            <div>
              <h2 className="text-xl font-bold">{threat.cveID}</h2>
              <p className="text-sm text-gray-600">{threat.vendorProject} Security Advisory</p>
            </div>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status and Badges */}
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant={getSeverityBadgeVariant(threat.severity)} className="text-sm">
              {threat.severity}
            </Badge>
            <Badge variant="outline">{threat.vendorProject}</Badge>
            {threat.knownRansomwareCampaignUse === 'Known' && (
              <Badge variant="destructive">
                <AlertTriangle className="h-3 w-3 mr-1" />
                Ransomware
              </Badge>
            )}
            <Badge variant="secondary">
              {threat.cwes.join(', ')}
            </Badge>
          </div>

          {/* Vulnerability Details */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Bug className="h-5 w-5 mr-2" />
                Vulnerability Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Vulnerability Name</h4>
                <p className="text-gray-700">{threat.vulnerabilityName}</p>
              </div>
              
              <div>
                <h4 className="font-semibold mb-2">Description</h4>
                <p className="text-gray-700">{threat.shortDescription}</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Affected Product</h4>
                  <p className="text-gray-700">{threat.product}</p>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-2">CWE Classification</h4>
                  <div className="flex flex-wrap gap-1">
                    {threat.cwes.map(cwe => (
                      <Badge key={cwe} variant="outline" className="text-xs">
                        {cwe}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Timeline and Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2" />
                  Timeline
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Date Added:</span>
                  <span className="text-sm text-gray-600">{threat.dateAdded}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Due Date:</span>
                  <span className="text-sm text-gray-600">{threat.dueDate}</span>
                </div>
                
                <Separator />
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Status:</span>
                  <span className={`text-sm ${urgencyColor}`}>
                    {daysUntilDue < 0 
                      ? `${Math.abs(daysUntilDue)} days overdue`
                      : daysUntilDue === 0
                      ? 'Due today'
                      : `${daysUntilDue} days remaining`
                    }
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Building className="h-5 w-5 mr-2" />
                  Threat Intelligence
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Ransomware Use:</span>
                  <Badge variant={threat.knownRansomwareCampaignUse === 'Known' ? 'destructive' : 'outline'}>
                    {threat.knownRansomwareCampaignUse}
                  </Badge>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Vendor:</span>
                  <span className="text-sm text-gray-600">{threat.vendorProject}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Severity Level:</span>
                  <Badge variant={getSeverityBadgeVariant(threat.severity)}>
                    {threat.severity}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Required Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2 text-orange-500" />
                Required Actions
              </CardTitle>
              <CardDescription>
                Immediate steps required to mitigate this vulnerability
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <p className="text-sm text-gray-700">{threat.requiredAction}</p>
              </div>
            </CardContent>
          </Card>

          {/* External Links */}
          <div className="flex flex-wrap gap-3">
            <Button onClick={openCVELink} variant="outline" size="sm">
              <ExternalLink className="h-4 w-4 mr-2" />
              View CVE Details
            </Button>
            
            <Button onClick={openVendorLink} variant="outline" size="sm">
              <ExternalLink className="h-4 w-4 mr-2" />
              Vendor Advisory
            </Button>
            
            <Button variant="outline" size="sm">
              <ExternalLink className="h-4 w-4 mr-2" />
              CISA Guidance
            </Button>
          </div>

          {/* Risk Assessment */}
          <Card className="border-l-4 border-l-red-500">
            <CardHeader>
              <CardTitle className="text-red-700">Risk Assessment</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="font-medium">Impact Level:</span>
                  <div className={`mt-1 ${threat.severity === 'Critical' ? 'text-red-600' : threat.severity === 'High' ? 'text-orange-600' : 'text-yellow-600'}`}>
                    {threat.severity}
                  </div>
                </div>
                
                <div>
                  <span className="font-medium">Exploitation:</span>
                  <div className="mt-1 text-gray-600">
                    {threat.knownRansomwareCampaignUse === 'Known' ? 'Active' : 'Potential'}
                  </div>
                </div>
                
                <div>
                  <span className="font-medium">Urgency:</span>
                  <div className={`mt-1 ${urgencyColor}`}>
                    {daysUntilDue <= 0 ? 'Immediate' : daysUntilDue <= 3 ? 'High' : 'Medium'}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <div className="flex justify-end space-x-3 p-6 border-t bg-gray-50">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
          <Button onClick={openCVELink}>
            <ExternalLink className="h-4 w-4 mr-2" />
            View Full Details
          </Button>
        </div>
      </div>
    </div>
  )
}

export default ThreatDetailsModal

