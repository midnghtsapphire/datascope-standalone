// API integration for Federal Cybersecurity Threat Intelligence Dashboard
// Connects to the DataScope Enhanced backend for real threat data

const API_BASE_URL = 'http://localhost:5000/api/v1'

class ThreatIntelligenceAPI {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async fetchThreats(filters = {}) {
    try {
      const queryParams = new URLSearchParams()
      
      // Add filters to query parameters
      if (filters.search) queryParams.append('search', filters.search)
      if (filters.vendor) queryParams.append('vendor', filters.vendor)
      if (filters.severity) queryParams.append('severity', filters.severity)
      if (filters.cwe) queryParams.append('cwe', filters.cwe)
      if (filters.dateRange) queryParams.append('date_range', filters.dateRange)
      if (filters.sortBy) queryParams.append('sort_by', filters.sortBy)
      if (filters.sortOrder) queryParams.append('sort_order', filters.sortOrder)
      if (filters.page) queryParams.append('page', filters.page)
      if (filters.limit) queryParams.append('limit', filters.limit)

      const response = await fetch(`${this.baseURL}/threats?${queryParams}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching threats:', error)
      // Return mock data as fallback
      return this.getMockData(filters)
    }
  }

  async fetchThreatById(cveId) {
    try {
      const response = await fetch(`${this.baseURL}/threats/${cveId}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching threat details:', error)
      return null
    }
  }

  async fetchAnalytics() {
    try {
      const response = await fetch(`${this.baseURL}/analytics`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Error fetching analytics:', error)
      return this.getMockAnalytics()
    }
  }

  async generateReport(reportType, filters = {}) {
    try {
      const response = await fetch(`${this.baseURL}/reports/${reportType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(filters)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      // Return blob for file download
      return await response.blob()
    } catch (error) {
      console.error('Error generating report:', error)
      throw error
    }
  }

  async exportData(format = 'json', filters = {}) {
    try {
      const queryParams = new URLSearchParams()
      queryParams.append('format', format)
      
      Object.entries(filters).forEach(([key, value]) => {
        if (value) queryParams.append(key, value)
      })

      const response = await fetch(`${this.baseURL}/export?${queryParams}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.blob()
    } catch (error) {
      console.error('Error exporting data:', error)
      throw error
    }
  }

  // Mock data fallback when API is not available
  getMockData(filters = {}) {
    const mockThreats = [
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
      }
    ]

    // Apply basic filtering
    let filtered = mockThreats
    
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase()
      filtered = filtered.filter(threat => 
        threat.cveID.toLowerCase().includes(searchTerm) ||
        threat.vendorProject.toLowerCase().includes(searchTerm) ||
        threat.product.toLowerCase().includes(searchTerm) ||
        threat.vulnerabilityName.toLowerCase().includes(searchTerm)
      )
    }
    
    if (filters.vendor && filters.vendor !== 'all') {
      filtered = filtered.filter(threat => threat.vendorProject === filters.vendor)
    }
    
    if (filters.severity && filters.severity !== 'all') {
      filtered = filtered.filter(threat => threat.severity === filters.severity)
    }

    return {
      threats: filtered,
      total: filtered.length,
      page: filters.page || 1,
      totalPages: Math.ceil(filtered.length / (filters.limit || 10))
    }
  }

  getMockAnalytics() {
    return {
      vendorStats: [
        { vendor: "Microsoft", count: 340 },
        { vendor: "Apple", count: 84 },
        { vendor: "Cisco", count: 80 },
        { vendor: "Adobe", count: 74 },
        { vendor: "Google", count: 65 }
      ],
      severityStats: [
        { severity: "Critical", count: 14 },
        { severity: "High", count: 12 },
        { severity: "Medium", count: 14 },
        { severity: "Low", count: 15 }
      ],
      cweStats: [
        { cwe: "CWE-119", count: 9 },
        { cwe: "CWE-20", count: 8 },
        { cwe: "CWE-79", count: 8 },
        { cwe: "CWE-22", count: 7 }
      ],
      timelineData: [
        { date: "2025-09-20", count: 2 },
        { date: "2025-09-21", count: 1 },
        { date: "2025-09-22", count: 4 },
        { date: "2025-09-23", count: 3 },
        { date: "2025-09-24", count: 2 },
        { date: "2025-09-25", count: 6 }
      ]
    }
  }
}

// Utility functions for data processing
export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export const getDaysUntilDue = (dueDate) => {
  const due = new Date(dueDate)
  const now = new Date()
  const diffTime = due - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays
}

export const getSeverityColor = (severity) => {
  switch (severity) {
    case 'Critical': return 'bg-red-500'
    case 'High': return 'bg-orange-500'
    case 'Medium': return 'bg-yellow-500'
    case 'Low': return 'bg-green-500'
    default: return 'bg-gray-500'
  }
}

export const getSeverityBadgeVariant = (severity) => {
  switch (severity) {
    case 'Critical': return 'destructive'
    case 'High': return 'destructive'
    case 'Medium': return 'secondary'
    case 'Low': return 'outline'
    default: return 'outline'
  }
}

export const getUrgencyColor = (daysUntilDue) => {
  if (daysUntilDue < 0) return 'text-red-600 font-bold'
  if (daysUntilDue <= 3) return 'text-orange-600 font-semibold'
  if (daysUntilDue <= 7) return 'text-yellow-600'
  return 'text-gray-600'
}

// Download helper function
export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.style.display = 'none'
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  window.URL.revokeObjectURL(url)
  document.body.removeChild(a)
}

// Create and export API instance
const threatAPI = new ThreatIntelligenceAPI()
export default threatAPI

