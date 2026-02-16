import { useState, useEffect, useMemo } from 'react'
import { Search, Filter, Download, AlertTriangle, Shield, Calendar, Building, Bug, TrendingUp, Eye, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import './App.css'

// Mock data - in production this would come from your API
const mockThreatData = [
  {
    cveID: "CVE-2025-20362",
    vendorProject: "Cisco",
    product: "Secure Firewall Adaptive Security Appliance",
    vulnerabilityName: "Cisco Secure Firewall Missing Authorization Vulnerability",
    dateAdded: "2025-09-25",
    dueDate: "2025-09-26",
    severity: "Critical",
    cwes: ["CWE-862"],
    shortDescription: "Missing authorization vulnerability that could be chained with CVE-2025-20333",
    knownRansomwareCampaignUse: "Unknown",
    requiredAction: "Apply mitigations per vendor instructions"
  },
  {
    cveID: "CVE-2025-20333",
    vendorProject: "Cisco",
    product: "Secure Firewall Threat Defense",
    vulnerabilityName: "Cisco Secure Firewall Buffer Overflow Vulnerability",
    dateAdded: "2025-09-25",
    dueDate: "2025-09-26",
    severity: "Critical",
    cwes: ["CWE-120"],
    shortDescription: "Buffer overflow vulnerability allowing remote code execution",
    knownRansomwareCampaignUse: "Unknown",
    requiredAction: "Apply mitigations per vendor instructions"
  },
  {
    cveID: "CVE-2025-10585",
    vendorProject: "Google",
    product: "Chromium V8",
    vulnerabilityName: "Google Chromium V8 Type Confusion Vulnerability",
    dateAdded: "2025-09-23",
    dueDate: "2025-10-14",
    severity: "High",
    cwes: ["CWE-843"],
    shortDescription: "Type confusion vulnerability in V8 JavaScript engine",
    knownRansomwareCampaignUse: "Unknown",
    requiredAction: "Apply mitigations per vendor instructions"
  },
  {
    cveID: "CVE-2025-5086",
    vendorProject: "Dassault Systèmes",
    product: "DELMIA Apriso",
    vulnerabilityName: "Dassault Systèmes DELMIA Apriso Deserialization Vulnerability",
    dateAdded: "2025-09-11",
    dueDate: "2025-10-02",
    severity: "High",
    cwes: ["CWE-502"],
    shortDescription: "Deserialization of untrusted data vulnerability leading to RCE",
    knownRansomwareCampaignUse: "Unknown",
    requiredAction: "Apply mitigations per vendor instructions"
  },
  {
    cveID: "CVE-2025-38352",
    vendorProject: "Linux",
    product: "Kernel",
    vulnerabilityName: "Linux Kernel TOCTOU Race Condition Vulnerability",
    dateAdded: "2025-09-04",
    dueDate: "2025-09-25",
    severity: "High",
    cwes: ["CWE-367"],
    shortDescription: "Time-of-check time-of-use race condition vulnerability",
    knownRansomwareCampaignUse: "Unknown",
    requiredAction: "Apply mitigations per vendor instructions"
  }
]

// Generate additional mock data for better visualization
const generateMockData = () => {
  const vendors = ["Microsoft", "Apple", "Adobe", "Oracle", "VMware", "Ivanti", "D-Link", "Apache"]
  const severities = ["Critical", "High", "Medium", "Low"]
  const cwes = ["CWE-20", "CWE-78", "CWE-787", "CWE-416", "CWE-119", "CWE-79", "CWE-89", "CWE-22"]
  
  const additionalData = []
  for (let i = 0; i < 50; i++) {
    const vendor = vendors[Math.floor(Math.random() * vendors.length)]
    const severity = severities[Math.floor(Math.random() * severities.length)]
    const cwe = cwes[Math.floor(Math.random() * cwes.length)]
    
    additionalData.push({
      cveID: `CVE-2025-${10000 + i}`,
      vendorProject: vendor,
      product: `${vendor} Product ${i}`,
      vulnerabilityName: `${vendor} ${severity} Vulnerability ${i}`,
      dateAdded: new Date(2025, 8, Math.floor(Math.random() * 25) + 1).toISOString().split('T')[0],
      dueDate: new Date(2025, 9, Math.floor(Math.random() * 30) + 1).toISOString().split('T')[0],
      severity: severity,
      cwes: [cwe],
      shortDescription: `Sample ${severity.toLowerCase()} vulnerability in ${vendor} product`,
      knownRansomwareCampaignUse: Math.random() > 0.8 ? "Known" : "Unknown",
      requiredAction: "Apply mitigations per vendor instructions"
    })
  }
  
  return [...mockThreatData, ...additionalData]
}

function App() {
  const [threats] = useState(generateMockData())
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedVendor, setSelectedVendor] = useState('all')
  const [selectedSeverity, setSelectedSeverity] = useState('all')
  const [selectedCWE, setSelectedCWE] = useState('all')
  const [dateRange, setDateRange] = useState('all')
  const [sortBy, setSortBy] = useState('dateAdded')
  const [sortOrder, setSortOrder] = useState('desc')
  const [selectedThreat, setSelectedThreat] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(10)

  // Filter and search logic
  const filteredThreats = useMemo(() => {
    let filtered = threats.filter(threat => {
      const matchesSearch = searchTerm === '' || 
        threat.cveID.toLowerCase().includes(searchTerm.toLowerCase()) ||
        threat.vendorProject.toLowerCase().includes(searchTerm.toLowerCase()) ||
        threat.product.toLowerCase().includes(searchTerm.toLowerCase()) ||
        threat.vulnerabilityName.toLowerCase().includes(searchTerm.toLowerCase())
      
      const matchesVendor = selectedVendor === 'all' || threat.vendorProject === selectedVendor
      const matchesSeverity = selectedSeverity === 'all' || threat.severity === selectedSeverity
      const matchesCWE = selectedCWE === 'all' || threat.cwes.includes(selectedCWE)
      
      let matchesDate = true
      if (dateRange !== 'all') {
        const threatDate = new Date(threat.dateAdded)
        const now = new Date()
        const daysAgo = parseInt(dateRange)
        const cutoffDate = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000))
        matchesDate = threatDate >= cutoffDate
      }
      
      return matchesSearch && matchesVendor && matchesSeverity && matchesCWE && matchesDate
    })

    // Sort the filtered results
    filtered.sort((a, b) => {
      let aValue = a[sortBy]
      let bValue = b[sortBy]
      
      if (sortBy === 'dateAdded' || sortBy === 'dueDate') {
        aValue = new Date(aValue)
        bValue = new Date(bValue)
      }
      
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return filtered
  }, [threats, searchTerm, selectedVendor, selectedSeverity, selectedCWE, dateRange, sortBy, sortOrder])

  // Pagination
  const totalPages = Math.ceil(filteredThreats.length / itemsPerPage)
  const paginatedThreats = filteredThreats.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  // Analytics data
  const vendorStats = useMemo(() => {
    const stats = {}
    threats.forEach(threat => {
      stats[threat.vendorProject] = (stats[threat.vendorProject] || 0) + 1
    })
    return Object.entries(stats)
      .map(([vendor, count]) => ({ vendor, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10)
  }, [threats])

  const severityStats = useMemo(() => {
    const stats = { Critical: 0, High: 0, Medium: 0, Low: 0 }
    threats.forEach(threat => {
      stats[threat.severity] = (stats[threat.severity] || 0) + 1
    })
    return Object.entries(stats).map(([severity, count]) => ({ severity, count }))
  }, [threats])

  const cweStats = useMemo(() => {
    const stats = {}
    threats.forEach(threat => {
      threat.cwes.forEach(cwe => {
        stats[cwe] = (stats[cwe] || 0) + 1
      })
    })
    return Object.entries(stats)
      .map(([cwe, count]) => ({ cwe, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8)
  }, [threats])

  const timelineData = useMemo(() => {
    const timeline = {}
    threats.forEach(threat => {
      const date = threat.dateAdded
      timeline[date] = (timeline[date] || 0) + 1
    })
    return Object.entries(timeline)
      .map(([date, count]) => ({ date, count }))
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(-30) // Last 30 days
  }, [threats])

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Critical': return 'bg-red-500'
      case 'High': return 'bg-orange-500'
      case 'Medium': return 'bg-yellow-500'
      case 'Low': return 'bg-green-500'
      default: return 'bg-gray-500'
    }
  }

  const getSeverityBadgeVariant = (severity) => {
    switch (severity) {
      case 'Critical': return 'destructive'
      case 'High': return 'destructive'
      case 'Medium': return 'secondary'
      case 'Low': return 'outline'
      default: return 'outline'
    }
  }

  const getDaysUntilDue = (dueDate) => {
    const due = new Date(dueDate)
    const now = new Date()
    const diffTime = due - now
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays
  }

  const getUrgencyColor = (daysUntilDue) => {
    if (daysUntilDue < 0) return 'text-red-600 font-bold'
    if (daysUntilDue <= 3) return 'text-orange-600 font-semibold'
    if (daysUntilDue <= 7) return 'text-yellow-600'
    return 'text-gray-600'
  }

  const uniqueVendors = [...new Set(threats.map(t => t.vendorProject))].sort()
  const uniqueCWEs = [...new Set(threats.flatMap(t => t.cwes))].sort()

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C']

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Shield className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Federal Cybersecurity Threat Intelligence</h1>
                <p className="text-sm text-gray-600">Real-time vulnerability monitoring and analysis</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-sm">
                <AlertTriangle className="h-4 w-4 mr-1" />
                {filteredThreats.length} Active Threats
              </Badge>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export Data
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="threats">Threat Database</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Threats</CardTitle>
                  <Bug className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{threats.length}</div>
                  <p className="text-xs text-muted-foreground">Active vulnerabilities</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Critical Threats</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">
                    {threats.filter(t => t.severity === 'Critical').length}
                  </div>
                  <p className="text-xs text-muted-foreground">Require immediate attention</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Overdue Actions</CardTitle>
                  <Calendar className="h-4 w-4 text-orange-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-600">
                    {threats.filter(t => getDaysUntilDue(t.dueDate) < 0).length}
                  </div>
                  <p className="text-xs text-muted-foreground">Past due date</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Affected Vendors</CardTitle>
                  <Building className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{uniqueVendors.length}</div>
                  <p className="text-xs text-muted-foreground">Unique vendors</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Critical Threats */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                  Recent Critical Threats
                </CardTitle>
                <CardDescription>
                  Latest critical vulnerabilities requiring immediate attention
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {threats
                    .filter(t => t.severity === 'Critical')
                    .slice(0, 5)
                    .map((threat) => (
                      <div key={threat.cveID} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <Badge variant="destructive">{threat.cveID}</Badge>
                            <Badge variant="outline">{threat.vendorProject}</Badge>
                          </div>
                          <h4 className="font-medium mt-2">{threat.vulnerabilityName}</h4>
                          <p className="text-sm text-gray-600 mt-1">{threat.shortDescription}</p>
                        </div>
                        <div className="text-right">
                          <div className={`text-sm ${getUrgencyColor(getDaysUntilDue(threat.dueDate))}`}>
                            {getDaysUntilDue(threat.dueDate) < 0 
                              ? `${Math.abs(getDaysUntilDue(threat.dueDate))} days overdue`
                              : `${getDaysUntilDue(threat.dueDate)} days remaining`
                            }
                          </div>
                          <div className="text-xs text-gray-500">Due: {threat.dueDate}</div>
                        </div>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Threats by Severity</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie
                        data={severityStats}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ severity, count }) => `${severity}: ${count}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {severityStats.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Top Affected Vendors</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={vendorStats.slice(0, 5)}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="vendor" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3B82F6" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Threats Tab */}
          <TabsContent value="threats" className="space-y-6">
            {/* Search and Filters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Filter className="h-5 w-5 mr-2" />
                  Search & Filter Threats
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      placeholder="Search CVE, vendor, product..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  
                  <Select value={selectedVendor} onValueChange={setSelectedVendor}>
                    <SelectTrigger>
                      <SelectValue placeholder="All Vendors" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Vendors</SelectItem>
                      {uniqueVendors.map(vendor => (
                        <SelectItem key={vendor} value={vendor}>{vendor}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  
                  <Select value={selectedSeverity} onValueChange={setSelectedSeverity}>
                    <SelectTrigger>
                      <SelectValue placeholder="All Severities" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Severities</SelectItem>
                      <SelectItem value="Critical">Critical</SelectItem>
                      <SelectItem value="High">High</SelectItem>
                      <SelectItem value="Medium">Medium</SelectItem>
                      <SelectItem value="Low">Low</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Select value={dateRange} onValueChange={setDateRange}>
                    <SelectTrigger>
                      <SelectValue placeholder="All Time" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Time</SelectItem>
                      <SelectItem value="7">Last 7 days</SelectItem>
                      <SelectItem value="30">Last 30 days</SelectItem>
                      <SelectItem value="90">Last 90 days</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">Sort by:</span>
                    <Select value={sortBy} onValueChange={setSortBy}>
                      <SelectTrigger className="w-40">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="dateAdded">Date Added</SelectItem>
                        <SelectItem value="dueDate">Due Date</SelectItem>
                        <SelectItem value="severity">Severity</SelectItem>
                        <SelectItem value="vendorProject">Vendor</SelectItem>
                      </SelectContent>
                    </Select>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                    >
                      {sortOrder === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </Button>
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    Showing {paginatedThreats.length} of {filteredThreats.length} threats
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Threats List */}
            <Card>
              <CardContent className="p-0">
                <div className="space-y-0">
                  {paginatedThreats.map((threat, index) => (
                    <div
                      key={threat.cveID}
                      className={`p-6 border-b cursor-pointer hover:bg-gray-50 transition-colors ${
                        index === paginatedThreats.length - 1 ? 'border-b-0' : ''
                      }`}
                      onClick={() => setSelectedThreat(selectedThreat?.cveID === threat.cveID ? null : threat)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <Badge variant="outline" className="font-mono">{threat.cveID}</Badge>
                            <Badge variant={getSeverityBadgeVariant(threat.severity)}>
                              {threat.severity}
                            </Badge>
                            <Badge variant="secondary">{threat.vendorProject}</Badge>
                            {threat.knownRansomwareCampaignUse === 'Known' && (
                              <Badge variant="destructive">Ransomware</Badge>
                            )}
                          </div>
                          
                          <h3 className="font-semibold text-lg mb-1">{threat.vulnerabilityName}</h3>
                          <p className="text-gray-600 mb-2">{threat.shortDescription}</p>
                          
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>Product: {threat.product}</span>
                            <span>Added: {threat.dateAdded}</span>
                            <span className={getUrgencyColor(getDaysUntilDue(threat.dueDate))}>
                              Due: {threat.dueDate}
                              {getDaysUntilDue(threat.dueDate) < 0 && ' (OVERDUE)'}
                            </span>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4 mr-1" />
                            Details
                          </Button>
                          <Button variant="outline" size="sm">
                            <ExternalLink className="h-4 w-4 mr-1" />
                            CVE
                          </Button>
                        </div>
                      </div>
                      
                      {selectedThreat?.cveID === threat.cveID && (
                        <div className="mt-4 pt-4 border-t bg-gray-50 -mx-6 px-6 py-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <h4 className="font-semibold mb-2">Vulnerability Details</h4>
                              <div className="space-y-2 text-sm">
                                <div><strong>CWE:</strong> {threat.cwes.join(', ')}</div>
                                <div><strong>Ransomware Use:</strong> {threat.knownRansomwareCampaignUse}</div>
                                <div><strong>Required Action:</strong> {threat.requiredAction}</div>
                              </div>
                            </div>
                            <div>
                              <h4 className="font-semibold mb-2">Timeline</h4>
                              <div className="space-y-2 text-sm">
                                <div><strong>Date Added:</strong> {threat.dateAdded}</div>
                                <div><strong>Due Date:</strong> {threat.dueDate}</div>
                                <div><strong>Days Remaining:</strong> 
                                  <span className={getUrgencyColor(getDaysUntilDue(threat.dueDate))}>
                                    {getDaysUntilDue(threat.dueDate) < 0 
                                      ? ` ${Math.abs(getDaysUntilDue(threat.dueDate))} days overdue`
                                      : ` ${getDaysUntilDue(threat.dueDate)} days`
                                    }
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>
                
                <div className="flex items-center space-x-1">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const page = i + 1
                    return (
                      <Button
                        key={page}
                        variant={currentPage === page ? "default" : "outline"}
                        size="sm"
                        onClick={() => setCurrentPage(page)}
                      >
                        {page}
                      </Button>
                    )
                  })}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Vendor Vulnerability Distribution</CardTitle>
                  <CardDescription>Top 10 vendors by vulnerability count</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={vendorStats}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="vendor" angle={-45} textAnchor="end" height={100} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3B82F6" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Vulnerability Types (CWE)</CardTitle>
                  <CardDescription>Most common vulnerability classifications</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={cweStats}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="cwe" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#10B981" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Threat Timeline</CardTitle>
                  <CardDescription>Vulnerabilities added over time</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={timelineData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Severity Distribution</CardTitle>
                  <CardDescription>Breakdown of threats by severity level</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={severityStats}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ severity, count, percent }) => `${severity}: ${count} (${(percent * 100).toFixed(0)}%)`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {severityStats.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Reports Tab */}
          <TabsContent value="reports" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Executive Summary</CardTitle>
                  <CardDescription>High-level threat overview for leadership</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Executive Report
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Technical Report</CardTitle>
                  <CardDescription>Detailed technical analysis for IT teams</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Technical Report
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Public Brief</CardTitle>
                  <CardDescription>Public-facing cybersecurity update</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Public Brief
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Vendor Report</CardTitle>
                  <CardDescription>Vendor-specific vulnerability analysis</CardDescription>
                </CardHeader>
                <CardContent>
                  <Select>
                    <SelectTrigger className="mb-3">
                      <SelectValue placeholder="Select Vendor" />
                    </SelectTrigger>
                    <SelectContent>
                      {uniqueVendors.map(vendor => (
                        <SelectItem key={vendor} value={vendor}>{vendor}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button className="w-full">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Vendor Report
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Compliance Report</CardTitle>
                  <CardDescription>Federal compliance and regulatory status</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <Download className="h-4 w-4 mr-2" />
                    Generate Compliance Report
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Custom Report</CardTitle>
                  <CardDescription>Build a custom report with specific filters</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <TrendingUp className="h-4 w-4 mr-2" />
                    Build Custom Report
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

