import typing_extensions

from tator_openapi.paths import PathValues
from tator_openapi.apis.paths.anonymous_gateway import AnonymousGateway
from tator_openapi.apis.paths.rest_affiliation_id import RestAffiliationId
from tator_openapi.apis.paths.rest_affiliations_organization import RestAffiliationsOrganization
from tator_openapi.apis.paths.rest_algorithm_id import RestAlgorithmId
from tator_openapi.apis.paths.rest_algorithm_launch_project import RestAlgorithmLaunchProject
from tator_openapi.apis.paths.rest_algorithms_project import RestAlgorithmsProject
from tator_openapi.apis.paths.rest_analyses_project import RestAnalysesProject
from tator_openapi.apis.paths.rest_analysis_id import RestAnalysisId
from tator_openapi.apis.paths.rest_announcement_id import RestAnnouncementId
from tator_openapi.apis.paths.rest_announcements import RestAnnouncements
from tator_openapi.apis.paths.rest_applet_id import RestAppletId
from tator_openapi.apis.paths.rest_applets_project import RestAppletsProject
from tator_openapi.apis.paths.rest_attribute_type_id import RestAttributeTypeId
from tator_openapi.apis.paths.rest_audio_file_id import RestAudioFileId
from tator_openapi.apis.paths.rest_audio_files_id import RestAudioFilesId
from tator_openapi.apis.paths.rest_auxiliary_file_id import RestAuxiliaryFileId
from tator_openapi.apis.paths.rest_auxiliary_files_id import RestAuxiliaryFilesId
from tator_openapi.apis.paths.rest_bookmark_id import RestBookmarkId
from tator_openapi.apis.paths.rest_bookmarks_project import RestBookmarksProject
from tator_openapi.apis.paths.rest_bucket_id import RestBucketId
from tator_openapi.apis.paths.rest_buckets_organization import RestBucketsOrganization
from tator_openapi.apis.paths.rest_change_log_project import RestChangeLogProject
from tator_openapi.apis.paths.rest_clone_media_project import RestCloneMediaProject
from tator_openapi.apis.paths.rest_download_info_project import RestDownloadInfoProject
from tator_openapi.apis.paths.rest_email_project import RestEmailProject
from tator_openapi.apis.paths.rest_favorite_id import RestFavoriteId
from tator_openapi.apis.paths.rest_favorites_project import RestFavoritesProject
from tator_openapi.apis.paths.rest_file_id import RestFileId
from tator_openapi.apis.paths.rest_file_type_id import RestFileTypeId
from tator_openapi.apis.paths.rest_file_types_project import RestFileTypesProject
from tator_openapi.apis.paths.rest_files_project import RestFilesProject
from tator_openapi.apis.paths.rest_get_clip_id import RestGetClipId
from tator_openapi.apis.paths.rest_get_cloned_media_id import RestGetClonedMediaId
from tator_openapi.apis.paths.rest_get_frame_id import RestGetFrameId
from tator_openapi.apis.paths.rest_image_file_id import RestImageFileId
from tator_openapi.apis.paths.rest_image_files_id import RestImageFilesId
from tator_openapi.apis.paths.rest_invitation_id import RestInvitationId
from tator_openapi.apis.paths.rest_invitations_organization import RestInvitationsOrganization
from tator_openapi.apis.paths.rest_job_uid import RestJobUid
from tator_openapi.apis.paths.rest_job_cluster_id import RestJobClusterId
from tator_openapi.apis.paths.rest_job_clusters_id import RestJobClustersId
from tator_openapi.apis.paths.rest_jobs_project import RestJobsProject
from tator_openapi.apis.paths.rest_leaf_id import RestLeafId
from tator_openapi.apis.paths.rest_leaf_count_project import RestLeafCountProject
from tator_openapi.apis.paths.rest_leaf_type_id import RestLeafTypeId
from tator_openapi.apis.paths.rest_leaf_types_project import RestLeafTypesProject
from tator_openapi.apis.paths.rest_leaves_suggestion_ancestor_project import RestLeavesSuggestionAncestorProject
from tator_openapi.apis.paths.rest_leaves_project import RestLeavesProject
from tator_openapi.apis.paths.rest_localization_id import RestLocalizationId
from tator_openapi.apis.paths.rest_localization_count_project import RestLocalizationCountProject
from tator_openapi.apis.paths.rest_localization_graphic_id import RestLocalizationGraphicId
from tator_openapi.apis.paths.rest_localization_type_id import RestLocalizationTypeId
from tator_openapi.apis.paths.rest_localization_types_project import RestLocalizationTypesProject
from tator_openapi.apis.paths.rest_localizations_project import RestLocalizationsProject
from tator_openapi.apis.paths.rest_media_id import RestMediaId
from tator_openapi.apis.paths.rest_media_count_project import RestMediaCountProject
from tator_openapi.apis.paths.rest_media_next_id import RestMediaNextId
from tator_openapi.apis.paths.rest_media_prev_id import RestMediaPrevId
from tator_openapi.apis.paths.rest_media_stats_project import RestMediaStatsProject
from tator_openapi.apis.paths.rest_media_type_id import RestMediaTypeId
from tator_openapi.apis.paths.rest_media_types_project import RestMediaTypesProject
from tator_openapi.apis.paths.rest_medias_project import RestMediasProject
from tator_openapi.apis.paths.rest_membership_id import RestMembershipId
from tator_openapi.apis.paths.rest_memberships_project import RestMembershipsProject
from tator_openapi.apis.paths.rest_merge_states_id import RestMergeStatesId
from tator_openapi.apis.paths.rest_notify import RestNotify
from tator_openapi.apis.paths.rest_organization_id import RestOrganizationId
from tator_openapi.apis.paths.rest_organization_upload_info_organization import RestOrganizationUploadInfoOrganization
from tator_openapi.apis.paths.rest_organizations import RestOrganizations
from tator_openapi.apis.paths.rest_password_reset import RestPasswordReset
from tator_openapi.apis.paths.rest_permalink_id import RestPermalinkId
from tator_openapi.apis.paths.rest_project_id import RestProjectId
from tator_openapi.apis.paths.rest_projects import RestProjects
from tator_openapi.apis.paths.rest_save_algorithm_manifest_project import RestSaveAlgorithmManifestProject
from tator_openapi.apis.paths.rest_save_generic_file_project import RestSaveGenericFileProject
from tator_openapi.apis.paths.rest_section_id import RestSectionId
from tator_openapi.apis.paths.rest_section_analysis_project import RestSectionAnalysisProject
from tator_openapi.apis.paths.rest_sections_project import RestSectionsProject
from tator_openapi.apis.paths.rest_state_id import RestStateId
from tator_openapi.apis.paths.rest_state_count_project import RestStateCountProject
from tator_openapi.apis.paths.rest_state_graphic_id import RestStateGraphicId
from tator_openapi.apis.paths.rest_state_type_id import RestStateTypeId
from tator_openapi.apis.paths.rest_state_types_project import RestStateTypesProject
from tator_openapi.apis.paths.rest_states_project import RestStatesProject
from tator_openapi.apis.paths.rest_temporary_file_id import RestTemporaryFileId
from tator_openapi.apis.paths.rest_temporary_files_project import RestTemporaryFilesProject
from tator_openapi.apis.paths.rest_token import RestToken
from tator_openapi.apis.paths.rest_transcode_project import RestTranscodeProject
from tator_openapi.apis.paths.rest_trim_state_end_id import RestTrimStateEndId
from tator_openapi.apis.paths.rest_upload_completion_project import RestUploadCompletionProject
from tator_openapi.apis.paths.rest_upload_info_project import RestUploadInfoProject
from tator_openapi.apis.paths.rest_user_exists import RestUserExists
from tator_openapi.apis.paths.rest_user_get_current import RestUserGetCurrent
from tator_openapi.apis.paths.rest_user_id import RestUserId
from tator_openapi.apis.paths.rest_users import RestUsers
from tator_openapi.apis.paths.rest_version_id import RestVersionId
from tator_openapi.apis.paths.rest_versions_project import RestVersionsProject
from tator_openapi.apis.paths.rest_video_file_id import RestVideoFileId
from tator_openapi.apis.paths.rest_video_files_id import RestVideoFilesId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.ANONYMOUSGATEWAY: AnonymousGateway,
        PathValues.REST_AFFILIATION_ID: RestAffiliationId,
        PathValues.REST_AFFILIATIONS_ORGANIZATION: RestAffiliationsOrganization,
        PathValues.REST_ALGORITHM_ID: RestAlgorithmId,
        PathValues.REST_ALGORITHM_LAUNCH_PROJECT: RestAlgorithmLaunchProject,
        PathValues.REST_ALGORITHMS_PROJECT: RestAlgorithmsProject,
        PathValues.REST_ANALYSES_PROJECT: RestAnalysesProject,
        PathValues.REST_ANALYSIS_ID: RestAnalysisId,
        PathValues.REST_ANNOUNCEMENT_ID: RestAnnouncementId,
        PathValues.REST_ANNOUNCEMENTS: RestAnnouncements,
        PathValues.REST_APPLET_ID: RestAppletId,
        PathValues.REST_APPLETS_PROJECT: RestAppletsProject,
        PathValues.REST_ATTRIBUTE_TYPE_ID: RestAttributeTypeId,
        PathValues.REST_AUDIO_FILE_ID: RestAudioFileId,
        PathValues.REST_AUDIO_FILES_ID: RestAudioFilesId,
        PathValues.REST_AUXILIARY_FILE_ID: RestAuxiliaryFileId,
        PathValues.REST_AUXILIARY_FILES_ID: RestAuxiliaryFilesId,
        PathValues.REST_BOOKMARK_ID: RestBookmarkId,
        PathValues.REST_BOOKMARKS_PROJECT: RestBookmarksProject,
        PathValues.REST_BUCKET_ID: RestBucketId,
        PathValues.REST_BUCKETS_ORGANIZATION: RestBucketsOrganization,
        PathValues.REST_CHANGE_LOG_PROJECT: RestChangeLogProject,
        PathValues.REST_CLONE_MEDIA_PROJECT: RestCloneMediaProject,
        PathValues.REST_DOWNLOAD_INFO_PROJECT: RestDownloadInfoProject,
        PathValues.REST_EMAIL_PROJECT: RestEmailProject,
        PathValues.REST_FAVORITE_ID: RestFavoriteId,
        PathValues.REST_FAVORITES_PROJECT: RestFavoritesProject,
        PathValues.REST_FILE_ID: RestFileId,
        PathValues.REST_FILE_TYPE_ID: RestFileTypeId,
        PathValues.REST_FILE_TYPES_PROJECT: RestFileTypesProject,
        PathValues.REST_FILES_PROJECT: RestFilesProject,
        PathValues.REST_GET_CLIP_ID: RestGetClipId,
        PathValues.REST_GET_CLONED_MEDIA_ID: RestGetClonedMediaId,
        PathValues.REST_GET_FRAME_ID: RestGetFrameId,
        PathValues.REST_IMAGE_FILE_ID: RestImageFileId,
        PathValues.REST_IMAGE_FILES_ID: RestImageFilesId,
        PathValues.REST_INVITATION_ID: RestInvitationId,
        PathValues.REST_INVITATIONS_ORGANIZATION: RestInvitationsOrganization,
        PathValues.REST_JOB_UID: RestJobUid,
        PathValues.REST_JOB_CLUSTER_ID: RestJobClusterId,
        PathValues.REST_JOB_CLUSTERS_ID: RestJobClustersId,
        PathValues.REST_JOBS_PROJECT: RestJobsProject,
        PathValues.REST_LEAF_ID: RestLeafId,
        PathValues.REST_LEAF_COUNT_PROJECT: RestLeafCountProject,
        PathValues.REST_LEAF_TYPE_ID: RestLeafTypeId,
        PathValues.REST_LEAF_TYPES_PROJECT: RestLeafTypesProject,
        PathValues.REST_LEAVES_SUGGESTION_ANCESTOR_PROJECT: RestLeavesSuggestionAncestorProject,
        PathValues.REST_LEAVES_PROJECT: RestLeavesProject,
        PathValues.REST_LOCALIZATION_ID: RestLocalizationId,
        PathValues.REST_LOCALIZATION_COUNT_PROJECT: RestLocalizationCountProject,
        PathValues.REST_LOCALIZATION_GRAPHIC_ID: RestLocalizationGraphicId,
        PathValues.REST_LOCALIZATION_TYPE_ID: RestLocalizationTypeId,
        PathValues.REST_LOCALIZATION_TYPES_PROJECT: RestLocalizationTypesProject,
        PathValues.REST_LOCALIZATIONS_PROJECT: RestLocalizationsProject,
        PathValues.REST_MEDIA_ID: RestMediaId,
        PathValues.REST_MEDIA_COUNT_PROJECT: RestMediaCountProject,
        PathValues.REST_MEDIA_NEXT_ID: RestMediaNextId,
        PathValues.REST_MEDIA_PREV_ID: RestMediaPrevId,
        PathValues.REST_MEDIA_STATS_PROJECT: RestMediaStatsProject,
        PathValues.REST_MEDIA_TYPE_ID: RestMediaTypeId,
        PathValues.REST_MEDIA_TYPES_PROJECT: RestMediaTypesProject,
        PathValues.REST_MEDIAS_PROJECT: RestMediasProject,
        PathValues.REST_MEMBERSHIP_ID: RestMembershipId,
        PathValues.REST_MEMBERSHIPS_PROJECT: RestMembershipsProject,
        PathValues.REST_MERGE_STATES_ID: RestMergeStatesId,
        PathValues.REST_NOTIFY: RestNotify,
        PathValues.REST_ORGANIZATION_ID: RestOrganizationId,
        PathValues.REST_ORGANIZATION_UPLOAD_INFO_ORGANIZATION: RestOrganizationUploadInfoOrganization,
        PathValues.REST_ORGANIZATIONS: RestOrganizations,
        PathValues.REST_PASSWORD_RESET: RestPasswordReset,
        PathValues.REST_PERMALINK_ID: RestPermalinkId,
        PathValues.REST_PROJECT_ID: RestProjectId,
        PathValues.REST_PROJECTS: RestProjects,
        PathValues.REST_SAVE_ALGORITHM_MANIFEST_PROJECT: RestSaveAlgorithmManifestProject,
        PathValues.REST_SAVE_GENERIC_FILE_PROJECT: RestSaveGenericFileProject,
        PathValues.REST_SECTION_ID: RestSectionId,
        PathValues.REST_SECTION_ANALYSIS_PROJECT: RestSectionAnalysisProject,
        PathValues.REST_SECTIONS_PROJECT: RestSectionsProject,
        PathValues.REST_STATE_ID: RestStateId,
        PathValues.REST_STATE_COUNT_PROJECT: RestStateCountProject,
        PathValues.REST_STATE_GRAPHIC_ID: RestStateGraphicId,
        PathValues.REST_STATE_TYPE_ID: RestStateTypeId,
        PathValues.REST_STATE_TYPES_PROJECT: RestStateTypesProject,
        PathValues.REST_STATES_PROJECT: RestStatesProject,
        PathValues.REST_TEMPORARY_FILE_ID: RestTemporaryFileId,
        PathValues.REST_TEMPORARY_FILES_PROJECT: RestTemporaryFilesProject,
        PathValues.REST_TOKEN: RestToken,
        PathValues.REST_TRANSCODE_PROJECT: RestTranscodeProject,
        PathValues.REST_TRIM_STATE_END_ID: RestTrimStateEndId,
        PathValues.REST_UPLOAD_COMPLETION_PROJECT: RestUploadCompletionProject,
        PathValues.REST_UPLOAD_INFO_PROJECT: RestUploadInfoProject,
        PathValues.REST_USER_EXISTS: RestUserExists,
        PathValues.REST_USER_GET_CURRENT: RestUserGetCurrent,
        PathValues.REST_USER_ID: RestUserId,
        PathValues.REST_USERS: RestUsers,
        PathValues.REST_VERSION_ID: RestVersionId,
        PathValues.REST_VERSIONS_PROJECT: RestVersionsProject,
        PathValues.REST_VIDEO_FILE_ID: RestVideoFileId,
        PathValues.REST_VIDEO_FILES_ID: RestVideoFilesId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.ANONYMOUSGATEWAY: AnonymousGateway,
        PathValues.REST_AFFILIATION_ID: RestAffiliationId,
        PathValues.REST_AFFILIATIONS_ORGANIZATION: RestAffiliationsOrganization,
        PathValues.REST_ALGORITHM_ID: RestAlgorithmId,
        PathValues.REST_ALGORITHM_LAUNCH_PROJECT: RestAlgorithmLaunchProject,
        PathValues.REST_ALGORITHMS_PROJECT: RestAlgorithmsProject,
        PathValues.REST_ANALYSES_PROJECT: RestAnalysesProject,
        PathValues.REST_ANALYSIS_ID: RestAnalysisId,
        PathValues.REST_ANNOUNCEMENT_ID: RestAnnouncementId,
        PathValues.REST_ANNOUNCEMENTS: RestAnnouncements,
        PathValues.REST_APPLET_ID: RestAppletId,
        PathValues.REST_APPLETS_PROJECT: RestAppletsProject,
        PathValues.REST_ATTRIBUTE_TYPE_ID: RestAttributeTypeId,
        PathValues.REST_AUDIO_FILE_ID: RestAudioFileId,
        PathValues.REST_AUDIO_FILES_ID: RestAudioFilesId,
        PathValues.REST_AUXILIARY_FILE_ID: RestAuxiliaryFileId,
        PathValues.REST_AUXILIARY_FILES_ID: RestAuxiliaryFilesId,
        PathValues.REST_BOOKMARK_ID: RestBookmarkId,
        PathValues.REST_BOOKMARKS_PROJECT: RestBookmarksProject,
        PathValues.REST_BUCKET_ID: RestBucketId,
        PathValues.REST_BUCKETS_ORGANIZATION: RestBucketsOrganization,
        PathValues.REST_CHANGE_LOG_PROJECT: RestChangeLogProject,
        PathValues.REST_CLONE_MEDIA_PROJECT: RestCloneMediaProject,
        PathValues.REST_DOWNLOAD_INFO_PROJECT: RestDownloadInfoProject,
        PathValues.REST_EMAIL_PROJECT: RestEmailProject,
        PathValues.REST_FAVORITE_ID: RestFavoriteId,
        PathValues.REST_FAVORITES_PROJECT: RestFavoritesProject,
        PathValues.REST_FILE_ID: RestFileId,
        PathValues.REST_FILE_TYPE_ID: RestFileTypeId,
        PathValues.REST_FILE_TYPES_PROJECT: RestFileTypesProject,
        PathValues.REST_FILES_PROJECT: RestFilesProject,
        PathValues.REST_GET_CLIP_ID: RestGetClipId,
        PathValues.REST_GET_CLONED_MEDIA_ID: RestGetClonedMediaId,
        PathValues.REST_GET_FRAME_ID: RestGetFrameId,
        PathValues.REST_IMAGE_FILE_ID: RestImageFileId,
        PathValues.REST_IMAGE_FILES_ID: RestImageFilesId,
        PathValues.REST_INVITATION_ID: RestInvitationId,
        PathValues.REST_INVITATIONS_ORGANIZATION: RestInvitationsOrganization,
        PathValues.REST_JOB_UID: RestJobUid,
        PathValues.REST_JOB_CLUSTER_ID: RestJobClusterId,
        PathValues.REST_JOB_CLUSTERS_ID: RestJobClustersId,
        PathValues.REST_JOBS_PROJECT: RestJobsProject,
        PathValues.REST_LEAF_ID: RestLeafId,
        PathValues.REST_LEAF_COUNT_PROJECT: RestLeafCountProject,
        PathValues.REST_LEAF_TYPE_ID: RestLeafTypeId,
        PathValues.REST_LEAF_TYPES_PROJECT: RestLeafTypesProject,
        PathValues.REST_LEAVES_SUGGESTION_ANCESTOR_PROJECT: RestLeavesSuggestionAncestorProject,
        PathValues.REST_LEAVES_PROJECT: RestLeavesProject,
        PathValues.REST_LOCALIZATION_ID: RestLocalizationId,
        PathValues.REST_LOCALIZATION_COUNT_PROJECT: RestLocalizationCountProject,
        PathValues.REST_LOCALIZATION_GRAPHIC_ID: RestLocalizationGraphicId,
        PathValues.REST_LOCALIZATION_TYPE_ID: RestLocalizationTypeId,
        PathValues.REST_LOCALIZATION_TYPES_PROJECT: RestLocalizationTypesProject,
        PathValues.REST_LOCALIZATIONS_PROJECT: RestLocalizationsProject,
        PathValues.REST_MEDIA_ID: RestMediaId,
        PathValues.REST_MEDIA_COUNT_PROJECT: RestMediaCountProject,
        PathValues.REST_MEDIA_NEXT_ID: RestMediaNextId,
        PathValues.REST_MEDIA_PREV_ID: RestMediaPrevId,
        PathValues.REST_MEDIA_STATS_PROJECT: RestMediaStatsProject,
        PathValues.REST_MEDIA_TYPE_ID: RestMediaTypeId,
        PathValues.REST_MEDIA_TYPES_PROJECT: RestMediaTypesProject,
        PathValues.REST_MEDIAS_PROJECT: RestMediasProject,
        PathValues.REST_MEMBERSHIP_ID: RestMembershipId,
        PathValues.REST_MEMBERSHIPS_PROJECT: RestMembershipsProject,
        PathValues.REST_MERGE_STATES_ID: RestMergeStatesId,
        PathValues.REST_NOTIFY: RestNotify,
        PathValues.REST_ORGANIZATION_ID: RestOrganizationId,
        PathValues.REST_ORGANIZATION_UPLOAD_INFO_ORGANIZATION: RestOrganizationUploadInfoOrganization,
        PathValues.REST_ORGANIZATIONS: RestOrganizations,
        PathValues.REST_PASSWORD_RESET: RestPasswordReset,
        PathValues.REST_PERMALINK_ID: RestPermalinkId,
        PathValues.REST_PROJECT_ID: RestProjectId,
        PathValues.REST_PROJECTS: RestProjects,
        PathValues.REST_SAVE_ALGORITHM_MANIFEST_PROJECT: RestSaveAlgorithmManifestProject,
        PathValues.REST_SAVE_GENERIC_FILE_PROJECT: RestSaveGenericFileProject,
        PathValues.REST_SECTION_ID: RestSectionId,
        PathValues.REST_SECTION_ANALYSIS_PROJECT: RestSectionAnalysisProject,
        PathValues.REST_SECTIONS_PROJECT: RestSectionsProject,
        PathValues.REST_STATE_ID: RestStateId,
        PathValues.REST_STATE_COUNT_PROJECT: RestStateCountProject,
        PathValues.REST_STATE_GRAPHIC_ID: RestStateGraphicId,
        PathValues.REST_STATE_TYPE_ID: RestStateTypeId,
        PathValues.REST_STATE_TYPES_PROJECT: RestStateTypesProject,
        PathValues.REST_STATES_PROJECT: RestStatesProject,
        PathValues.REST_TEMPORARY_FILE_ID: RestTemporaryFileId,
        PathValues.REST_TEMPORARY_FILES_PROJECT: RestTemporaryFilesProject,
        PathValues.REST_TOKEN: RestToken,
        PathValues.REST_TRANSCODE_PROJECT: RestTranscodeProject,
        PathValues.REST_TRIM_STATE_END_ID: RestTrimStateEndId,
        PathValues.REST_UPLOAD_COMPLETION_PROJECT: RestUploadCompletionProject,
        PathValues.REST_UPLOAD_INFO_PROJECT: RestUploadInfoProject,
        PathValues.REST_USER_EXISTS: RestUserExists,
        PathValues.REST_USER_GET_CURRENT: RestUserGetCurrent,
        PathValues.REST_USER_ID: RestUserId,
        PathValues.REST_USERS: RestUsers,
        PathValues.REST_VERSION_ID: RestVersionId,
        PathValues.REST_VERSIONS_PROJECT: RestVersionsProject,
        PathValues.REST_VIDEO_FILE_ID: RestVideoFileId,
        PathValues.REST_VIDEO_FILES_ID: RestVideoFilesId,
    }
)
